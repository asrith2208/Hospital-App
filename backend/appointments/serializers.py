from rest_framework import serializers
from .models import Appointment
from users.serializers import UserSerializer
from departments.serializers import DepartmentSerializer

class AppointmentSerializer(serializers.ModelSerializer):
    patient = UserSerializer(read_only=True)
    doctor = UserSerializer(read_only=True)
    department = DepartmentSerializer(read_only=True)
    class Meta:
        model = Appointment
        fields = ['id', 'patient', 'doctor', 'department', 'date', 'time_slot', 'status', 'reason', 'created_at', 'updated_at'] 