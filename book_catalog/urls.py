from django.contrib import admin
from django.urls import path
from .views import BookListView, BookDetailView, ReviewCreateView, BookUpdateView

urlpatterns = [
    path('', BookListView.as_view()),
    path('<int:pk>', BookDetailView.as_view(), name='book-detail'),
    path('<int:review_book>/review', ReviewCreateView.as_view(), name='review-create'),
    path('<int:pk>/update', BookUpdateView.as_view(), name='update-favorite'),
]
