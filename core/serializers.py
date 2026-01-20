from rest_framework import serializers
from .models import ContactMessage, ProfileInfo, Experience, Education, Skill, Certification


class ContactMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactMessage
        fields = ['id', 'name', 'email', 'subject', 'message', 'created_at']
        read_only_fields = ['id', 'created_at']


class ExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Experience
        fields = ['id', 'title', 'company', 'period', 'description', 'order']


class EducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Education
        fields = ['id', 'degree', 'institution', 'year', 'grade', 'description', 'order']


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ['id', 'name', 'category', 'proficiency', 'order']


class CertificationSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='title', read_only=True)  # Alias for frontend compatibility
    
    class Meta:
        model = Certification
        fields = ['id', 'name', 'title', 'issuer', 'date', 'description', 'credential_url', 'order']


class ProfileInfoSerializer(serializers.ModelSerializer):
    experiences = serializers.SerializerMethodField()
    education = serializers.SerializerMethodField()
    skills = serializers.SerializerMethodField()
    certifications = serializers.SerializerMethodField()
    
    class Meta:
        model = ProfileInfo
        fields = [
            'id', 'full_name', 'title', 'bio', 'about', 'achievements', 'profile_image', 'cv_link',
            'email', 'phone', 'website', 'location',
            'github_url', 'linkedin_url', 'twitter_url', 'facebook_url',
            'experiences', 'education', 'skills', 'certifications',
            'updated_at'
        ]
    
    def get_experiences(self, obj):
        experiences = Experience.objects.all()
        return ExperienceSerializer(experiences, many=True).data
    
    def get_education(self, obj):
        education = Education.objects.all()
        return EducationSerializer(education, many=True).data
    
    def get_skills(self, obj):
        skills = Skill.objects.all()
        return SkillSerializer(skills, many=True).data
    
    def get_certifications(self, obj):
        certifications = Certification.objects.all()
        return CertificationSerializer(certifications, many=True).data


class ProfileInfoWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfileInfo
        fields = [
            'full_name', 'title', 'bio', 'about', 'achievements', 'profile_image', 'cv_link',
            'email', 'phone', 'website', 'location',
            'github_url', 'linkedin_url', 'twitter_url', 'facebook_url'
        ]
