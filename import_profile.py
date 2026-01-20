"""
Script to import profile, experience, education, skills, and certifications data
"""
import os
import sys
import django

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
django.setup()

from core.models import ProfileInfo, Experience, Education, Skill, Certification


def import_profile_data():
    print("=" * 60)
    print("  IMPORTING PROFILE DATA")
    print("=" * 60)
    
    # Create or update profile
    profile, created = ProfileInfo.objects.get_or_create(
        id=1,
        defaults={
            'full_name': 'Abdullah Noman',
            'title': 'Textile Engineer',
            'bio': 'I am a passionate and dedicated Textile Engineer with comprehensive expertise in Yarn manufacturing, quality control systems, and production process optimization.',
            'about': 'I am deeply committed to sustainable practices and continuous improvement in textile manufacturing. My work focuses on integrating modern technology with traditional craftsmanship to create innovative, eco-friendly solutions that meet the evolving demands of the global textile industry.',
            'achievements': ['Completed a thesis on fiber & Yarn recycling technologies'],
            'email': 'abdullahnoman001@gmail.com',
            'location': 'Dhaka, Bangladesh',
            'github_url': 'https://github.com/shahriartamim2',
            'linkedin_url': 'https://www.linkedin.com/in/me-noman/',
            'cv_link': 'https://drive.google.com/file/d/1GgY1vCvPXyzL5BR1pGJ_vFK1wvikM66v/view',
        }
    )
    if created:
        print(f"  ✓ Created profile: {profile.full_name}")
    else:
        print(f"  ✓ Profile already exists: {profile.full_name}")
    
    # Import experiences
    print("\nImporting experiences...")
    experiences_data = [
        {
            'title': 'Intern',
            'company': 'Mosaraf Composite Textile Mills Ltd',
            'period': 'August 2025 - September 2025',
            'description': 'Gained hands-on experience in various textile manufacturing processes, including spinning, knitting, dyeing, and finishing. Assisted in quality control and production planning activities.',
            'order': 1,
        },
    ]
    
    for exp_data in experiences_data:
        exp, created = Experience.objects.get_or_create(
            title=exp_data['title'],
            company=exp_data['company'],
            defaults=exp_data
        )
        action = "Created" if created else "Already exists"
        print(f"  ✓ {action}: {exp.title} at {exp.company}")
    
    # Import education
    print("\nImporting education...")
    education_data = [
        {
            'degree': 'B.Sc. in Textile Engineering',
            'institution': 'Bangladesh University of Textiles (BUTEX)',
            'year': '2026 (Expected)',
            'grade': 'CGPA - 3.21',
            'description': 'Specialized in Yarn Manufacturing',
            'order': 1,
        },
        {
            'degree': 'Higher Secondary Certificate (HSC)',
            'institution': 'Govt. KC College, Jhenidah',
            'year': '2019',
            'grade': 'GPA - 5.00',
            'description': 'Science',
            'order': 2,
        },
        {
            'degree': 'Secondary School Certificate (SSC)',
            'institution': 'Joradah Secondary School, Harinakundu',
            'year': '2017',
            'grade': 'GPA - 5.00',
            'description': 'Science',
            'order': 3,
        },
    ]
    
    for edu_data in education_data:
        edu, created = Education.objects.get_or_create(
            degree=edu_data['degree'],
            institution=edu_data['institution'],
            defaults=edu_data
        )
        action = "Created" if created else "Already exists"
        print(f"  ✓ {action}: {edu.degree}")
    
    # Import skills
    print("\nImporting skills...")
    skills_data = [
        # Technical Skills
        {'name': 'Quality Control Systems', 'category': 'technical', 'order': 1},
        {'name': 'Fabric Analysis', 'category': 'technical', 'order': 2},
        {'name': 'Production Planning', 'category': 'technical', 'order': 3},
        {'name': 'Process Engineering', 'category': 'technical', 'order': 4},
        {'name': 'Process Optimization', 'category': 'technical', 'order': 5},
        # Specialized Skills
        {'name': 'Dyeing & Finishing Technology', 'category': 'specialized', 'order': 1},
        {'name': 'Fabric Testing Standards', 'category': 'specialized', 'order': 2},
        {'name': 'Yarn Manufacturing', 'category': 'specialized', 'order': 3},
        {'name': 'Fabric Manufacturing', 'category': 'specialized', 'order': 4},
        {'name': 'ISO Quality Standards', 'category': 'specialized', 'order': 5},
        # Software Skills
        {'name': 'Excel', 'category': 'software', 'order': 1},
        {'name': 'Word', 'category': 'software', 'order': 2},
        {'name': 'PowerBI', 'category': 'software', 'order': 3},
        {'name': 'MS Access', 'category': 'software', 'order': 4},
        {'name': 'SPSS', 'category': 'software', 'order': 5},
        {'name': 'R Studio', 'category': 'software', 'order': 6},
        {'name': 'Python', 'category': 'software', 'order': 7},
    ]
    
    for skill_data in skills_data:
        skill, created = Skill.objects.get_or_create(
            name=skill_data['name'],
            defaults=skill_data
        )
        action = "Created" if created else "Already exists"
        print(f"  ✓ {action}: {skill.name} ({skill.category})")
    
    # Import certifications
    print("\nImporting certifications...")
    certifications_data = [
        {'title': 'ICPC Dhaka Regional Finalist 2024', 'issuer': 'ICPC', 'order': 1},
        {'title': 'Python for Data Science & AI', 'issuer': 'Coursera', 'order': 2},
        {'title': 'Python Course Offered by University of Michigan', 'issuer': 'University of Michigan', 'order': 3},
        {'title': 'Management', 'issuer': '', 'order': 4},
    ]
    
    for cert_data in certifications_data:
        cert, created = Certification.objects.get_or_create(
            title=cert_data['title'],
            defaults=cert_data
        )
        action = "Created" if created else "Already exists"
        print(f"  ✓ {action}: {cert.title}")
    
    print("\n" + "=" * 60)
    print("  ✓ Profile data import completed!")
    print("=" * 60)
    
    # Summary
    print(f"\nDatabase Summary:")
    print(f"  - Profile: {ProfileInfo.objects.count()}")
    print(f"  - Experiences: {Experience.objects.count()}")
    print(f"  - Education: {Education.objects.count()}")
    print(f"  - Skills: {Skill.objects.count()}")
    print(f"  - Certifications: {Certification.objects.count()}")


if __name__ == '__main__':
    import_profile_data()
