from rest_framework import serializers
from django.db.models import Avg
from .models import Genre, Author, Book, Review, FavoriteBook


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'


class BookSerializer(serializers.ModelSerializer):
    is_favorite = serializers.SerializerMethodField()
    rating = serializers.SerializerMethodField()
    author_name = serializers.CharField(source='author.name', read_only=True)
    genre_name = serializers.CharField(source='genre.name', read_only=True)
    
    class Meta:
        model = Book
        fields = ['id', 'title', 'genre_name', 
                  'author_name', 'is_favorite', 'rating',
        ]

    def get_is_favorite(self, obj):
        user = self.context['request'].user
        return FavoriteBook.objects.filter(user=user, book=obj).exists()
    
    def get_rating(self, obj):
        return Review.objects.filter(book=obj).aggregate(Avg('rating'))['rating__avg']
    
    
class FavoriteBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavoriteBook
        fields = '__all__'
