from rest_framework import generics, mixins, viewsets
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend

from book.service import BookFilter
from .models import Book, Review, FavoriteBook
from .serializers import BookSerializer, ReviewSerializer, FavoriteBookSerializer, BookDetailSerializer


class BookViewSet(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """Детальный просмотр книг"""
    
    queryset = Book.objects.all()
    serializer_class = BookDetailSerializer
    
    
class BookListView(generics.ListAPIView):
    """Главная страница с фильтрацией"""
    
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = (DjangoFilterBackend, )
    filterset_class = BookFilter


class ReviewViewSet(viewsets.ModelViewSet):
    """ViewSet для комментариев"""
    
    permission_classes = [IsAuthenticated]
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer


class FavoriteBookViewSet(viewsets.ModelViewSet):
    """ViewSet для избранных книг"""
    
    permission_classes = [IsAuthenticated]
    queryset = FavoriteBook.objects.all()
    serializer_class = FavoriteBookSerializer


