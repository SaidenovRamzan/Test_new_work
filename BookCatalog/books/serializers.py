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
    reviews = ReviewSerializer(many=True, read_only=True)
    is_favorite = serializers.SerializerMethodField()
    rating = serializers.SerializerMethodField()
    genre = GenreSerializer()
    author = AuthorSerializer()
    
    class Meta:
        model = Book
        fields = ['id', 'title', 'genre', 
                  'author', 'publication_date', 'description', 
                  'reviews', 'is_favorite', 'rating',
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
