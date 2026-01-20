"""
Create demo categories for the portfolio application.
Run: python manage.py shell < create_demo_categories.py
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from blogs.models import Category

# Demo categories for a Textile Engineer / Developer portfolio
demo_categories = [
    # Tech/Development categories
    {"name": "Web Development", "slug": "web-development"},
    {"name": "React", "slug": "react"},
    {"name": "Python", "slug": "python"},
    {"name": "Django", "slug": "django"},
    {"name": "JavaScript", "slug": "javascript"},
    {"name": "Frontend", "slug": "frontend"},
    {"name": "Backend", "slug": "backend"},
    {"name": "Full Stack", "slug": "full-stack"},
    {"name": "UI/UX Design", "slug": "ui-ux-design"},
    {"name": "Mobile Development", "slug": "mobile-development"},
    
    # Textile/Industry categories
    {"name": "Textile Engineering", "slug": "textile-engineering"},
    {"name": "Fabric Technology", "slug": "fabric-technology"},
    {"name": "Yarn Manufacturing", "slug": "yarn-manufacturing"},
    {"name": "Quality Control", "slug": "quality-control"},
    {"name": "Sustainable Fashion", "slug": "sustainable-fashion"},
    {"name": "Industrial Automation", "slug": "industrial-automation"},
    
    # General categories
    {"name": "Tutorial", "slug": "tutorial"},
    {"name": "Project", "slug": "project"},
    {"name": "Case Study", "slug": "case-study"},
    {"name": "Research", "slug": "research"},
    {"name": "Portfolio", "slug": "portfolio"},
    {"name": "Personal", "slug": "personal"},
    {"name": "Career", "slug": "career"},
    {"name": "News", "slug": "news"},
]

created_count = 0
existing_count = 0

for cat_data in demo_categories:
    category, created = Category.objects.get_or_create(
        slug=cat_data["slug"],
        defaults={"name": cat_data["name"]}
    )
    if created:
        print(f"✓ Created: {category.name}")
        created_count += 1
    else:
        print(f"  Already exists: {category.name}")
        existing_count += 1

print(f"\n{'='*40}")
print(f"Summary: {created_count} created, {existing_count} already existed")
print(f"Total categories: {Category.objects.count()}")
