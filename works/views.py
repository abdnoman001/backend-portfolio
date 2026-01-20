from rest_framework import viewsets, filters
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser
from django.db.models import F
from .models import Work
from .serializers import WorkListSerializer, WorkAdminListSerializer, WorkDetailSerializer, WorkWriteSerializer


class WorkViewSet(viewsets.ModelViewSet):
    """
    ViewSet for portfolio works/projects.
    Public: GET (list, detail)
    Admin only: POST, PUT, PATCH, DELETE
    """
    queryset = Work.objects.filter(is_published=True)
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'description']
    ordering_fields = ['order', 'created_at', 'views']
    ordering = ['order']
    
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
        raise NotFound('Work not found')
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Admin can see all works, public users only published
        if self.request.user.is_staff:
            queryset = Work.objects.all()
        
        # Filter by category
        category = self.request.query_params.get('category', None)
        if category:
            queryset = queryset.filter(category__slug=category)
        
        return queryset
    
    def get_serializer_class(self):
        if self.action == 'list':
            # Use admin serializer with full data for staff users
            if self.request.user.is_staff:
                return WorkAdminListSerializer
            return WorkListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return WorkWriteSerializer
        return WorkDetailSerializer
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdminUser()]
        return super().get_permissions()
    
    def retrieve(self, request, *args, **kwargs):
        """Increment view count on work detail retrieval"""
        instance = self.get_object()
        
        # Increment views
        Work.objects.filter(pk=instance.pk).update(views=F('views') + 1)
        instance.refresh_from_db()
        
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
