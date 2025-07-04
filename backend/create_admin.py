import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'titikshahospitals@gmail.com', 'bella@2208')
    print("Superuser created.")
else:
    print("Superuser already exists.") 