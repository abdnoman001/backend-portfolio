from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser
from django.db.models import F
from .models import Category, Blog
from .serializers import (
    CategorySerializer, 
    BlogListSerializer, 
    BlogAdminListSerializer,
    BlogDetailSerializer, 
    BlogWriteSerializer
)


class CategoryViewSet(viewsets.ModelViewSet):
    """
    ViewSet for listing categories.
    Public: Read-only access
    Admin: Full CRUD
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdminUser()]
        return []


class BlogViewSet(viewsets.ModelViewSet):
    """
    ViewSet for blog posts.
    Public: GET (list, detail)
    Admin only: POST, PUT, PATCH, DELETE
    """
    queryset = Blog.objects.filter(is_published=True)
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'description', 'content']
    ordering_fields = ['date', 'views', 'created_at']
    ordering = ['-date']
    
    def get_object(self):
        """Support lookup by either ID or slug"""
        lookup_value = self.kwargs.get('pk')
        queryset = self.get_queryset()
        
        # Try to lookup by ID first (if numeric)
        if lookup_value.isdigit():
            obj = queryset.filter(pk=lookup_value).first()
            if obj:
                self.check_object_permissions(self.request, obj)
                return obj
        
        # Fall back to slug lookup
        obj = queryset.filter(slug=lookup_value).first()
        if obj:
            self.check_object_permissions(self.request, obj)
            return obj
        
        from rest_framework.exceptions import NotFound
        raise NotFound('Blog not found')
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Admin can see all blogs, public users only published
        if self.request.user.is_staff:
            queryset = Blog.objects.all()
        
        # Filter by category
        category = self.request.query_params.get('category', None)
        if category:
            queryset = queryset.filter(category__slug=category)
        
        return queryset
    
    def get_serializer_class(self):
        if self.action == 'list':
            # Use admin serializer with full data for staff users
            if self.request.user.is_staff:
                return BlogAdminListSerializer
            return BlogListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return BlogWriteSerializer
        return BlogDetailSerializer
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdminUser()]
        return super().get_permissions()
    
    def retrieve(self, request, *args, **kwargs):
        """Increment view count on blog detail retrieval"""
        instance = self.get_object()
        
        # Increment views
        Blog.objects.filter(pk=instance.pk).update(views=F('views') + 1)
        instance.refresh_from_db()
        
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
