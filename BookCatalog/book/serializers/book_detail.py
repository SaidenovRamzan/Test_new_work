from rest_framework import serializers
from django.db.models import Avg
from book.models import Book, Review, FavoriteBook
from accounts.service import get_user_from_token


class CommentSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='user.email', read_only=True)
    book_title = serializers.CharField(source='book.title', read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'text', 'author_name', 'book_title', 'rating']


class BookDetailSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)
    author_name = serializers.CharField(source='author.name', read_only=True)
    genre_name = serializers.CharField(source='genre.name', read_only=True)
    rating = serializers.SerializerMethodField()
    is_favorite = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = ['id', 'title', 'genre_name', 'author_name', 'rating', 'is_favorite', 'comments',]

    def get_is_favorite(self, obj) -> bool:
        user = get_user_from_token(self.context['request'])
        if not user:
            return False
        try:
            return FavoriteBook.objects.filter(user=user, book=obj).exists()
        except: return False
        
    def get_rating(self, obj) -> float:
        try:
            return Review.objects.filter(book=obj).aggregate(Avg('rating'))['rating__avg']
        except: return None
        

    