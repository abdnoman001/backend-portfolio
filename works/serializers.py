from rest_framework import serializers
from .models import Work, WorkImage, WorkSection
from blogs.models import Category
from blogs.serializers import CategorySerializer


class WorkImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkImage
        fields = ['id', 'image', 'order', 'caption']


class WorkSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkSection
        fields = ['id', 'title', 'description', 'image', 'order']


class WorkListSerializer(serializers.ModelSerializer):
    """Serializer for work list view"""
    category_name = serializers.CharField(source='category.name', read_only=True, default='')
    
    class Meta:
        model = Work
        fields = ['id', 'title', 'slug', 'description', 'image', 'category_name', 'link']


class WorkAdminListSerializer(serializers.ModelSerializer):
    """Serializer for admin work list - includes all fields needed for editing"""
    category_name = serializers.CharField(source='category.name', read_only=True, default='')
    category = CategorySerializer(read_only=True)
    images = WorkImageSerializer(many=True, read_only=True)
    sections = WorkSectionSerializer(many=True, read_only=True)
    
    class Meta:
        model = Work
        fields = [
            'id', 'title', 'slug', 'description', 'image', 'images',
            'sections', 'category', 'category_name', 'link', 'is_published', 
            'order', 'views', 'created_at', 'updated_at'
        ]


class WorkDetailSerializer(serializers.ModelSerializer):
    """Serializer for work detail view with nested images and sections"""
    category_name = serializers.CharField(source='category.name', read_only=True, default='')
    category = CategorySerializer(read_only=True)
    images = WorkImageSerializer(many=True, read_only=True)
    sections = WorkSectionSerializer(many=True, read_only=True)
    
    class Meta:
        model = Work
        fields = [
            'id', 'title', 'slug', 'description', 'image', 'images',
            'sections', 'category', 'category_name', 'link', 'views', 'created_at', 'updated_at'
        ]


class WorkWriteSerializer(serializers.ModelSerializer):
    """Serializer for creating/updating works (admin only)"""
    images = WorkImageSerializer(many=True, required=False)
    sections = WorkSectionSerializer(many=True, required=False)
    
    class Meta:
        model = Work
        fields = [
            'id', 'title', 'slug', 'description', 'image', 
            'category', 'link', 'is_published', 'order', 'images', 'sections'
        ]
        extra_kwargs = {
            'slug': {'required': False}
        }
    
    def create(self, validated_data):
        images_data = validated_data.pop('images', [])
        sections_data = validated_data.pop('sections', [])
        
        work = Work.objects.create(**validated_data)
        
        for image_data in images_data:
            WorkImage.objects.create(work=work, **image_data)
        
        for section_data in sections_data:
            WorkSection.objects.create(work=work, **section_data)
        
        return work
    
    def update(self, instance, validated_data):
        images_data = validated_data.pop('images', None)
        sections_data = validated_data.pop('sections', None)
        
        # Update work fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        # Update images if provided
        if images_data is not None:
            instance.images.all().delete()
            for image_data in images_data:
                WorkImage.objects.create(work=instance, **image_data)
        
        # Update sections if provided
        if sections_data is not None:
            instance.sections.all().delete()
            for section_data in sections_data:
                WorkSection.objects.create(work=instance, **section_data)
        
        return instance
