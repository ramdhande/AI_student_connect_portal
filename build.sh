#!/usr/bin/env bash
# exit on error
set -o errexit

echo "=== Installing dependencies ==="
pip install -r requirements.txt

echo "=== Collecting static files ==="
python student_connect_portal/manage.py collectstatic --noinput --clear

echo "=== Build finished successfully ==="
