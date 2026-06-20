#!/usr/bin/env bash
# exit on error
set -o errexit

echo "=== Running Database Migrations ==="
python student_connect_portal/manage.py migrate --noinput

echo "=== Checking and Seeding Database if Empty ==="
python -c "
import os, sys, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'student_connect_portal.settings')
django.setup()
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.exists():
    print('Database is empty. Seeding data...')
    sys.path.append('student_connect_portal')
    import seed_db
    seed_db.seed()
else:
    print('Database already contains data. Skipping seeding.')
"

echo "=== Starting WSGI Server with Gunicorn ==="
gunicorn --chdir student_connect_portal student_connect_portal.wsgi:application --bind 0.0.0.0:$PORT
