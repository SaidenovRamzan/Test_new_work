from rest_framework import serializers
from django.db.models import Avg

from book.models import Review, FavoriteBook, Book
from accounts.service import get_user_from_token


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'
        
    
class FavoriteBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavoriteBook
        fields = '__all__'
        
        
class BookSerializer(serializers.ModelSerializer):
    is_favorite = serializers.SerializerMethodField()
    rating = serializers.SerializerMethodField()
    author_name = serializers.CharField(source='author.name', read_only=True)
    genre_name = serializers.CharField(source='genre.name', read_only=True)
    detail = serializers.HyperlinkedIdentityField(view_name='book-detail', format='html')
    
    class Meta:
        model = Book
        fields = ['id', 'title', 'genre_name', 'author_name', 'is_favorite', 'rating', 'detail']

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
        
