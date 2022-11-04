from django_filters import rest_framework as filters

from .models import Book


class CharFilterInFilter(filters.BaseInFilter, filters.CharFilter):
    """Additional filter for ManyToMany fields"""
    pass


class BooksFilter(filters.FilterSet):
    """Filter for BookListView"""
    book_genre = CharFilterInFilter(field_name='book_genre__genre_name', lookup_expr='in')
    book_author = CharFilterInFilter(field_name='book_author__author_name', lookup_expr='in')
    book_date_min = filters.DateFilter(field_name='book_date', lookup_expr='gte')
    book_date_max = filters.DateFilter(field_name='book_date', lookup_expr='lte')

    class Meta:
        model = Book
        fields = ('book_genre', 'book_author',)
