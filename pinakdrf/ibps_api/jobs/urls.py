# jobs/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('status/', views.api_status, name='api-status'),
    path('login/', views.login_view, name='login'),
    path('jobs/', views.job_listings_view, name='job-listings'),
    path('jobs/add/', views.add_job_view, name='add-job'),
]