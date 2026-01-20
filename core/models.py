from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class ContactMessage(models.Model):
    """Contact form submissions"""
    name = models.CharField(max_length=255)
    email = models.EmailField()
    subject = models.CharField(max_length=255)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['is_read']),
        ]
    
    def __str__(self):
        return f"{self.name} - {self.subject}"


class ProfileInfo(models.Model):
    """Singleton model for profile/about information"""
    # Personal Info
    full_name = models.CharField(max_length=255, default="Abdullah Noman")
    title = models.CharField(max_length=255, default="Textile Engineer")
    bio = models.TextField(help_text="Short bio/tagline")
    about = models.TextField(help_text="Detailed about me description", blank=True)
    achievements = models.JSONField(default=list, blank=True, help_text="List of achievements")
    profile_image = models.URLField(max_length=500, blank=True)
    cv_link = models.URLField(max_length=500, blank=True)
    
    # Contact Info
    email = models.EmailField(default="abdnoman001@gmail.com")
    phone = models.CharField(max_length=50, blank=True)
    website = models.URLField(max_length=500, blank=True)
    location = models.CharField(max_length=255, blank=True)
    
    # Social Links
    github_url = models.URLField(max_length=500, blank=True)
    linkedin_url = models.URLField(max_length=500, blank=True)
    twitter_url = models.URLField(max_length=500, blank=True)
    facebook_url = models.URLField(max_length=500, blank=True)
    
    # Meta
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Profile Information"
        verbose_name_plural = "Profile Information"
    
    def save(self, *args, **kwargs):
        # Ensure only one instance exists
        if not self.pk and ProfileInfo.objects.exists():
            raise ValueError("Only one ProfileInfo instance is allowed")
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"Profile: {self.full_name}"


class Experience(models.Model):
    """Work experience entries"""
    title = models.CharField(max_length=255)
    company = models.CharField(max_length=255)
    period = models.CharField(max_length=100, help_text="e.g., 'June 2024 - July 2024'")
    description = models.TextField()
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['order', '-created_at']
    
    def __str__(self):
        return f"{self.title} at {self.company}"


class Education(models.Model):
    """Education entries"""
    degree = models.CharField(max_length=255)
    institution = models.CharField(max_length=255)
    year = models.CharField(max_length=100)
    grade = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['order', '-created_at']
        verbose_name_plural = "Education"
    
    def __str__(self):
        return f"{self.degree} - {self.institution}"


class Skill(models.Model):
    """Skills organized by category"""
    CATEGORY_CHOICES = [
        ('technical', 'Technical Skills'),
        ('specialized', 'Specialized Skills'),
        ('software', 'Software & Tools'),
        ('other', 'Other'),
    ]
    
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='technical')
    proficiency = models.IntegerField(
        default=50,
        help_text="Proficiency level (0-100)",
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['category', 'order', 'name']
    
    def __str__(self):
        return f"{self.name} ({self.get_category_display()})"


class Certification(models.Model):
    """Certifications and achievements"""
    title = models.CharField(max_length=255)
    issuer = models.CharField(max_length=255, blank=True)
    date = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    credential_url = models.URLField(max_length=500, blank=True)
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['order', '-created_at']
    
    def __str__(self):
        return self.title
