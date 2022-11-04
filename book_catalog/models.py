from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class User(AbstractUser):
    pass


class Author(models.Model):
    """Author model"""
    author_name = models.CharField("Author name", max_length=200)

    def __str__(self):
        return self.author_name


class Genre(models.Model):
    """Genre model"""
    genre_name = models.CharField("Genre", max_length=200)

    def __str__(self):
        return self.genre_name


class Book(models.Model):
    """Book model"""
    book_name = models.CharField("Book name", max_length=200)
    book_date = models.DateField("Publication date")
    book_description = models.TextField("Book description")
    book_author = models.ManyToManyField(Author, verbose_name="authors")
    book_genre = models.ManyToManyField(Genre, verbose_name="genre")
    book_favorite = models.ManyToManyField(User, related_name="favorite_books", blank=True)

    def __str__(self):
        return self.book_name


class Review(models.Model):
    """Review model"""
    review_description = models.TextField("Review")
    review_book_rating = models.SmallIntegerField("Rating", default=0,
                                                  validators=(MinValueValidator(0), MaxValueValidator(10)))
    review_book = models.ForeignKey(Book, related_name="book_rating", on_delete=models.CASCADE, default=None)
    review_user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'Review to {self.review_book}'
