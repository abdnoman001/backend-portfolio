from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, BlogViewSet

router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'', BlogViewSet, basename='blog')

urlpatterns = [
    path('', include(router.urls)),
]
