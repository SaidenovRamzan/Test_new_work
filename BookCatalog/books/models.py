from django.db import models
from django.contrib.auth.models import User


class Genre(models.Model):
    """Жанры книги"""
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Author(models.Model):
    """Авторы книги"""
    name = models.CharField(max_length=255)
    birth_date = models.DateField()

    def __str__(self):
        return self.name


class Book(models.Model):
    """Книга"""
    title = models.CharField(max_length=255)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    publication_date = models.DateField("Дата выхода")
    description = models.TextField()

    def __str__(self):
        return self.title


class Review(models.Model):
    """Коментарии к книге"""
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField()
    text = models.TextField()

    def __str__(self):
        return f"{self.user.username} - {self.book.title}"


class FavoriteBook(models.Model):
    """Избранные книги"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} - {self.book.title}"
