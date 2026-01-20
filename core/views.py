from rest_framework import viewsets, generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAdminUser
from .models import ContactMessage, ProfileInfo, Experience, Education, Skill, Certification
from .serializers import (
    ContactMessageSerializer, 
    ProfileInfoSerializer, 
    ProfileInfoWriteSerializer,
    ExperienceSerializer,
    EducationSerializer,
    SkillSerializer,
    CertificationSerializer
)


class ContactMessageViewSet(viewsets.ModelViewSet):
    """
    ViewSet for contact messages.
    Public: POST (create)
    Admin only: GET (list), DELETE
    """
    queryset = ContactMessage.objects.all()
    serializer_class = ContactMessageSerializer
    
    def get_permissions(self):
        if self.action == 'create':
            return [AllowAny()]
        return [IsAdminUser()]
    
    def create(self, request, *args, **kwargs):
        """Allow public to submit contact messages"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(
            {"message": "Your message has been sent successfully!"},
            status=status.HTTP_201_CREATED
        )


class ProfileInfoView(generics.RetrieveUpdateAPIView):
    """
    View for profile information.
    Public: GET
    Admin only: PUT, PATCH
    """
    queryset = ProfileInfo.objects.all()
    
    def get_object(self):
        """Return the single ProfileInfo instance or create one"""
        profile, created = ProfileInfo.objects.get_or_create(id=1)
        return profile
    
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ProfileInfoSerializer
        return ProfileInfoWriteSerializer
    
    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAdminUser()]


class ExperienceViewSet(viewsets.ModelViewSet):
    """Admin-only CRUD for experiences"""
    queryset = Experience.objects.all()
    serializer_class = ExperienceSerializer
    permission_classes = [IsAdminUser]


class EducationViewSet(viewsets.ModelViewSet):
    """Admin-only CRUD for education"""
    queryset = Education.objects.all()
    serializer_class = EducationSerializer
    permission_classes = [IsAdminUser]


class SkillViewSet(viewsets.ModelViewSet):
    """Admin-only CRUD for skills"""
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer
    permission_classes = [IsAdminUser]


class CertificationViewSet(viewsets.ModelViewSet):
    """Admin-only CRUD for certifications"""
    queryset = Certification.objects.all()
    serializer_class = CertificationSerializer
    permission_classes = [IsAdminUser]
