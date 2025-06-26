from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLE_CHOICES = (
        ('patient', 'Patient'),
        ('doctor', 'Doctor'),
        ('admin', 'Admin'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='patient')
    # You can add more fields if needed (e.g., phone number)

class DoctorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='doctor_profile')
    specialty = models.CharField(max_length=100)
    bio = models.TextField(blank=True)
    experience = models.PositiveIntegerField(default=0)
    profile_pic = models.ImageField(upload_to='doctor_profiles/', blank=True, null=True)
    # Add more fields as needed (e.g., availability)

class PatientProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='patient_profile')
    address = models.CharField(max_length=255)
    medical_history = models.TextField(blank=True)
    allergies = models.CharField(max_length=255, blank=True)
    medications = models.CharField(max_length=255, blank=True)
    emergency_contact = models.CharField(max_length=100, blank=True)
    profile_pic = models.ImageField(upload_to='patient_profiles/', blank=True, null=True)
    # Add more fields as needed
