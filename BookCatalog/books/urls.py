from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    GenreViewSet, AuthorViewSet, BookViewSet, 
    ReviewViewSet, FavoriteBookViewSet, BookListView
)

router = DefaultRouter()
router.register(r'genres', GenreViewSet)
router.register(r'authors', AuthorViewSet)
router.register(r'books', BookViewSet)
router.register(r'reviews', ReviewViewSet)
router.register(r'favorites', FavoriteBookViewSet, basename='favoritebook')

urlpatterns = [
    path('api/v1/', include(router.urls)),
    path('', BookListView.as_view())
]
