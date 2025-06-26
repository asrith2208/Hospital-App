from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse

def home(request):
    return HttpResponse("Hospital App Backend is Live!")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('users.urls')),
    path('api/departments/', include('departments.urls')),
    path('api/appointments/', include('appointments.urls')),
    path('', home),
]
