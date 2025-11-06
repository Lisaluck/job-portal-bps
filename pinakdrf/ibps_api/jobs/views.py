# jobs/views.py
import jwt
import datetime
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from .models import JobListing

# Simple JWT implementation
JWT_SECRET = 'ibps-jwt-secret-key-2024-change-in-production'


@api_view(['GET'])
@permission_classes([AllowAny])
def api_status(request):
    """API status check endpoint"""
    return Response({
        'success': True,
        'message': 'IBPS Jobs API is running',
        'version': '1.0.0',
        'endpoints': {
            'login': '/api/login/',
            'jobs': '/api/jobs/',
            'add_job': '/api/jobs/add/',
            'status': '/api/status/'
        }
    })


@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    """Login endpoint"""
    username = request.data.get('username')
    password = request.data.get('password')

    if not username or not password:
        return Response(
            {'success': False, 'error': 'Username and password required'},
            status=status.HTTP_400_BAD_REQUEST
        )

    # Test credentials
    test_credentials = [
        {'username': 'testuser', 'password': 'testpass123'},
        {'username': 'admin', 'password': 'admin123'},
        {'username': 'ibps', 'password': 'ibps123'}
    ]

    for cred in test_credentials:
        if username == cred['username'] and password == cred['password']:
            # Create or get user
            user, created = User.objects.get_or_create(
                username=cred['username'],
                defaults={
                    'email': f'{cred["username"]}@example.com',
                    'is_staff': False,
                    'is_superuser': False
                }
            )
            if created:
                user.set_password(cred['password'])
                user.save()

            # Generate JWT token
            payload = {
                'user_id': user.id,
                'username': user.username,
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1),
                'iat': datetime.datetime.utcnow()
            }

            token = jwt.encode(payload, JWT_SECRET, algorithm='HS256')

            return Response({
                'success': True,
                'token': token,
                'user': {
                    'id': user.id,
                    'username': user.username,
                },
                'message': 'Login successful'
            })

    return Response(
        {'success': False, 'error': 'Invalid credentials'},
        status=status.HTTP_401_UNAUTHORIZED
    )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def job_listings_view(request):
    """Get all job listings"""
    jobs = JobListing.objects.all()

    # Agar koi job na ho toh sample data add karein
    if not jobs.exists():
        sample_jobs = [
            JobListing(
                title='IBPS PO Recruitment 2024',
                location='All India',
                post_date='2024-01-15',
                link='https://www.ibps.in/po-recruitment-2024'
            ),
            JobListing(
                title='IBPS Clerk Notification 2024',
                location='Multiple Locations',
                post_date='2024-01-10',
                link='https://www.ibps.in/clerk-2024'
            ),
            JobListing(
                title='IBPS SO Recruitment 2024',
                location='All India',
                post_date='2024-01-05',
                link='https://www.ibps.in/so-recruitment-2024'
            )
        ]
        JobListing.objects.bulk_create(sample_jobs)
        jobs = JobListing.objects.all()

    # Simple response without serializer
    job_data = []
    for job in jobs:
        job_data.append({
            'id': job.id,
            'title': job.title,
            'location': job.location,
            'post_date': job.post_date,
            'link': job.link,
            'created_at': job.created_at
        })

    return Response({
        'success': True,
        'count': len(job_data),
        'jobs': job_data
    })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_job_view(request):
    """Add new job listing"""
    title = request.data.get('title')
    location = request.data.get('location', 'All India')
    post_date = request.data.get('post_date')
    link = request.data.get('link')

    if not title or not post_date or not link:
        return Response({
            'success': False,
            'error': 'Title, post_date and link are required'
        }, status=status.HTTP_400_BAD_REQUEST)

    job = JobListing.objects.create(
        title=title,
        location=location,
        post_date=post_date,
        link=link
    )

    return Response({
        'success': True,
        'message': 'Job added successfully',
        'job': {
            'id': job.id,
            'title': job.title,
            'location': job.location,
            'post_date': job.post_date,
            'link': job.link
        }
    })