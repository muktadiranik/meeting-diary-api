# !/bin/bash

# Start the Celery worker
celery -A backend worker -l info &

# Start the Django server
python manage.py runserver
