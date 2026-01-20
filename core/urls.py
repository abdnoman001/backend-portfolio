from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ContactMessageViewSet, 
    ProfileInfoView,
    ExperienceViewSet,
    EducationViewSet,
    SkillViewSet,
    CertificationViewSet
)

router = DefaultRouter()
router.register(r'contact-messages', ContactMessageViewSet, basename='contact-message')
router.register(r'experiences', ExperienceViewSet, basename='experience')
router.register(r'education', EducationViewSet, basename='education')
router.register(r'skills', SkillViewSet, basename='skill')
router.register(r'certifications', CertificationViewSet, basename='certification')

urlpatterns = [
    # Public contact form submission + Admin list/delete
    path('contact/', ContactMessageViewSet.as_view({
        'post': 'create',
        'get': 'list',
    }), name='contact'),
    path('contact/<int:pk>/', ContactMessageViewSet.as_view({
        'get': 'retrieve',
        'patch': 'partial_update',
        'delete': 'destroy',
    }), name='contact-detail'),
    path('profile/', ProfileInfoView.as_view(), name='profile-info'),
    path('', include(router.urls)),
]
