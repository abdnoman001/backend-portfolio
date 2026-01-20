from rest_framework import serializers
from .models import Category, Blog


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug']


class BlogListSerializer(serializers.ModelSerializer):
    """Serializer for blog list view"""
    category_name = serializers.CharField(source='category.name', read_only=True, default='')
    
    class Meta:
        model = Blog
        fields = ['id', 'title', 'slug', 'description', 'date', 'image', 'category_name', 'views']


class BlogAdminListSerializer(serializers.ModelSerializer):
    """Serializer for admin blog list - includes all fields needed for editing"""
    category_name = serializers.CharField(source='category.name', read_only=True, default='')
    category = CategorySerializer(read_only=True)
    
    class Meta:
        model = Blog
        fields = [
            'id', 'title', 'slug', 'description', 'content', 
            'date', 'image', 'category', 'category_name', 'is_published', 'views', 
            'created_at', 'updated_at'
        ]


class BlogDetailSerializer(serializers.ModelSerializer):
    """Serializer for blog detail view"""
    category_name = serializers.CharField(source='category.name', read_only=True, default='')
    category = CategorySerializer(read_only=True)
    
    class Meta:
        model = Blog
        fields = [
            'id', 'title', 'slug', 'description', 'content', 
            'date', 'image', 'category', 'category_name', 'views', 'created_at', 'updated_at'
        ]


class BlogWriteSerializer(serializers.ModelSerializer):
    """Serializer for creating/updating blogs (admin only)"""
    class Meta:
        model = Blog
        fields = [
            'id', 'title', 'slug', 'description', 'content', 
            'date', 'image', 'category', 'is_published'
        ]
        extra_kwargs = {
            'slug': {'required': False}
        }
