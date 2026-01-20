from django.contrib import admin
from .models import Work, WorkImage, WorkSection


class WorkImageInline(admin.TabularInline):
    model = WorkImage
    extra = 1
    fields = ['image', 'order', 'caption']


class WorkSectionInline(admin.StackedInline):
    model = WorkSection
    extra = 1
    fields = ['title', 'description', 'image', 'order']


@admin.register(Work)
class WorkAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'is_published', 'order', 'views', 'created_at']
    list_filter = ['is_published', 'category']
    search_fields = ['title', 'description']
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ['views', 'created_at', 'updated_at']
    inlines = [WorkImageInline, WorkSectionInline]
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'category', 'order', 'is_published')
        }),
        ('Content', {
            'fields': ('description', 'image', 'link')
        }),
        ('Metadata', {
            'fields': ('views', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(WorkImage)
class WorkImageAdmin(admin.ModelAdmin):
    list_display = ['work', 'order', 'caption', 'created_at']
    list_filter = ['work']
    search_fields = ['work__title', 'caption']


@admin.register(WorkSection)
class WorkSectionAdmin(admin.ModelAdmin):
    list_display = ['work', 'title', 'order', 'created_at']
    list_filter = ['work']
    search_fields = ['work__title', 'title', 'description']
