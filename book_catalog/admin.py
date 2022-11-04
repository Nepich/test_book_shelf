from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.db import models

from .models import Book, Genre, Author, Review, User

# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(Review)


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    """Admin Book"""
    list_display = ('book_name', 'book_date')
    list_filter = ('book_name', 'book_date')
    search_fields = ('book_name', 'book_date')


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    """Admin Authors"""
    list_display = ('author_name',)
    search_fields = ('author_name',)


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    """Admin Genres"""
    list_display = ('genre_name',)
    search_fields = ('genre_name',)

