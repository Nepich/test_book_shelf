from rest_framework import serializers

from .models import Book, Review, User


class UserSerializer(serializers.ModelSerializer):
    """User serializer"""
    class Meta:
        model = User
        fields = ('id',)


class ReviewListSerializer(serializers.ModelSerializer):
    """Rating serializer"""
    review_user = serializers.SlugRelatedField(slug_field="username", read_only=True)

    class Meta:
        model = Review
        exclude = ('id', 'review_book')


class ReviewCreateSerializer(serializers.ModelSerializer):
    """Rating create serializer"""
    review_user = serializers.PrimaryKeyRelatedField(read_only=True)
    review_book = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Review
        fields = '__all__'


class BookListSerializer(serializers.ModelSerializer):
    """Book list serializer"""
    book_genre = serializers.SlugRelatedField(slug_field="genre_name", read_only=True, many=True)
    book_author = serializers.SlugRelatedField(slug_field="author_name", read_only=True, many=True)
    book_detail_url = serializers.HyperlinkedIdentityField(view_name='book-detail', read_only=True)
    book_rating = serializers.SlugRelatedField(slug_field="review_book_rating", read_only=True, many=True)

    def to_representation(self, instance):
        """Overrides default values"""
        representation = super().to_representation(instance)
        if representation['book_rating']:
            representation['book_rating'] = sum(representation['book_rating'])/len(representation['book_rating'])
        user = self.context['request'].user
        if self.context['request'].user.is_authenticated:
            representation['book_favorite'] = True if user.id in representation['book_favorite'] else False
        else:
            representation['book_favorite'] = None
        return representation

    class Meta:
        model = Book
        exclude = ('book_description', 'id', 'book_date')


class BookDetailSerializer(serializers.ModelSerializer):
    """Book detail serializer"""
    book_genre = serializers.SlugRelatedField(slug_field="genre_name", read_only=True, many=True)
    book_author = serializers.SlugRelatedField(slug_field="author_name", read_only=True, many=True)
    book_rating = ReviewListSerializer(read_only=True, many=True)

    class Meta:
        model = Book
        exclude = ('id',)


class BookDetailUpdateSerializer(serializers.ModelSerializer):
    """Book detail serializer"""

    class Meta:
        model = Book
        fields = ('book_favorite',)


