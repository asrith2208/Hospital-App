from django.shortcuts import render
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Appointment
from .serializers import AppointmentSerializer
from users.models import User
from django.core.mail import send_mail
from django.conf import settings
from datetime import timedelta
from django.utils import timezone

# Create your views here.

class AppointmentListCreateView(generics.ListCreateAPIView):
    serializer_class = AppointmentSerializer
    permission_classes = [permissions.IsAuthenticated]
    def get_queryset(self):
        user = self.request.user
        if user.role == 'patient':
            return Appointment.objects.filter(patient=user)
        elif user.role == 'doctor':
            return Appointment.objects.filter(doctor=user)
        elif user.role == 'admin':
            return Appointment.objects.all()
        return Appointment.objects.none()
    def perform_create(self, serializer):
        user = self.request.user
        if user.role == 'patient':
            appointment = serializer.save(patient=user)
            # Send confirmation email to patient and doctor
            send_mail(
                subject='Appointment Confirmation',
                message=f'Your appointment with Dr. {appointment.doctor.get_full_name()} is confirmed for {appointment.date} at {appointment.time_slot}.',
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[appointment.patient.email, appointment.doctor.email],
                fail_silently=True,
            )
        else:
            appointment = serializer.save()

class AppointmentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    permission_classes = [permissions.IsAuthenticated]
    def delete(self, request, *args, **kwargs):
        appointment = self.get_object()
        user = request.user
        if user.role == 'patient' and appointment.patient != user:
            return Response({'error': 'Not allowed'}, status=status.HTTP_403_FORBIDDEN)
        return super().delete(request, *args, **kwargs)

# (Optional) You can add a management command or scheduled task for reminders
# Example skeleton for sending reminders 24 hours before appointment:
def send_appointment_reminders():
    now = timezone.now()
    tomorrow = now + timedelta(days=1)
    appointments = Appointment.objects.filter(date=tomorrow.date(), status='confirmed')
    for appointment in appointments:
        send_mail(
            subject='Appointment Reminder',
            message=f'Reminder: You have an appointment with Dr. {appointment.doctor.get_full_name()} on {appointment.date} at {appointment.time_slot}.',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[appointment.patient.email],
            fail_silently=True,
        )
