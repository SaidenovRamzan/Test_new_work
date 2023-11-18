from rest_framework import generics
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend

from books.service import BookFilter
from .models import Genre, Author, Book, Review, FavoriteBook
from .serializers import GenreSerializer, AuthorSerializer, BookSerializer, ReviewSerializer, FavoriteBookSerializer


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer


class FavoriteBookViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = FavoriteBookSerializer

    def get_queryset(self):
        return FavoriteBook.objects.filter(user=self.request.user)


class BookListView(generics.ListAPIView):
    """Главная страница с фильтрацией"""
    
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = (DjangoFilterBackend, )
    filterset_class = BookFilter
