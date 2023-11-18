from django.contrib import admin
from books.models import (
    Genre, Author, Book, 
    Review, FavoriteBook
)

admin.site.register(Genre)
admin.site.register(Author)
admin.site.register(Book)
admin.site.register(Review)
admin.site.register(FavoriteBook)





