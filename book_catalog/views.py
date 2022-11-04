from copy import deepcopy

from django.contrib import auth
from django.db.models import Q
from rest_framework import serializers, permissions
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView, UpdateAPIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response

from .models import Book, Review, User
from .serializers import BookListSerializer, BookDetailSerializer, ReviewCreateSerializer, BookDetailUpdateSerializer
from .service import BooksFilter


class BookListView(ListAPIView):
    """Views a list of books"""
    queryset = Book.objects.all()
    serializer_class = BookListSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = BooksFilter


class BookDetailView(RetrieveAPIView):
    """Views a details of book"""
    queryset = Book.objects.all()
    serializer_class = BookDetailSerializer


class BookUpdateView(UpdateAPIView):
    """Updates favorite for a book"""
    queryset = Book.objects.all()
    serializer_class = BookDetailUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request, *args, **kwargs):
        """Adds a book to favorites or removes it from there"""
        obj = Book.objects.get(pk=self.kwargs.get(self.lookup_field))
        username = self.request.user
        if obj.book_favorite.filter(username=username):
            obj.book_favorite.set(obj.book_favorite.filter(~Q(username=username)))
            obj.save()
        else:
            self.update(request, *args, **kwargs)
        serializer = BookDetailUpdateSerializer(obj)
        return Response(serializer.data)


class ReviewCreateView(CreateAPIView):
    """Creating a review for a book"""
    serializer_class = ReviewCreateSerializer
    queryset = Review.objects.all()
    lookup_url_kwarg = "review_book"
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        """Adding review_user and review_book fields and checking unique"""
        uid = self.kwargs.get(self.lookup_url_kwarg)
        user_data = self.request.user
        queryset_values = self.get_queryset().values()
        if queryset_values:
            print(queryset_values)
            for queryset_value in queryset_values:
                if Book.objects.get(pk=uid).id == queryset_value['review_book_id'] and\
                        user_data.id == queryset_value['review_user_id']:
                    raise serializers.ValidationError('Only single review allowed')
        serializer.save(review_user=user_data, review_book=Book.objects.get(pk=uid),)








