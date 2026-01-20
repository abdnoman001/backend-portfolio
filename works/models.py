from django.db import models
from django.utils.text import slugify
from blogs.models import Category


class Work(models.Model):
    """Portfolio work/project model"""
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    description = models.TextField(help_text="Brief project description")
    image = models.URLField(max_length=500, help_text="Main/cover image URL")
    category = models.ForeignKey(
        Category, 
        on_delete=models.SET_NULL, 
        null=True, 
        related_name='works'
    )
    link = models.URLField(max_length=500, blank=True, help_text="External project link (optional)")
    is_published = models.BooleanField(default=True)
    order = models.IntegerField(default=0, help_text="Display order (lower numbers appear first)")
    views = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['order', '-created_at']
        indexes = [
            models.Index(fields=['order']),
            models.Index(fields=['slug']),
        ]
    
    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            while Work.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.title


class WorkImage(models.Model):
    """Additional images for work gallery"""
    work = models.ForeignKey(Work, on_delete=models.CASCADE, related_name='images')
    image = models.URLField(max_length=500, help_text="Gallery image URL")
    order = models.IntegerField(default=0)
    caption = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['order', 'id']
    
    def __str__(self):
        return f"{self.work.title} - Image {self.order}"


class WorkSection(models.Model):
    """Detailed feature sections for work"""
    work = models.ForeignKey(Work, on_delete=models.CASCADE, related_name='sections')
    title = models.CharField(max_length=255, blank=True, help_text="Section heading (optional)")
    description = models.TextField(help_text="Section content/feature description")
    image = models.URLField(max_length=500, help_text="Section image URL")
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['order', 'id']
    
    def __str__(self):
        return f"{self.work.title} - {self.title or f'Section {self.order}'}"
