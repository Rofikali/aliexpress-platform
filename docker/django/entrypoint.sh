#!/bin/sh
set -e

echo "🔄 Applying database migrations..."
python manage.py makemigrations products shared --noinput
python manage.py migrate --noinput

echo "📦 Collecting static files..."
python manage.py collectstatic --noinput

echo "👤 Ensuring admin user exists..."
python manage.py shell <<EOF
from django.contrib.auth import get_user_model
import os

User = get_user_model()

username = os.environ.get("DJANGO_SUPERUSER_USERNAME", "admin")
email = os.environ.get("DJANGO_SUPERUSER_EMAIL", "admin@gmail.com")
password = os.environ.get("DJANGO_SUPERUSER_PASSWORD", "admin12345")

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(
        username=username,
        email=email,
        password=password,
    )
    print("✅ Superuser created")
else:
    print("ℹ️ Superuser already exists")
EOF

echo "🚀 Starting Gunicorn..."
exec gunicorn config.wsgi:application \
  --bind 0.0.0.0:8000 \
  --workers 4
