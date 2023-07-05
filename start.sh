# !/bin/bash

# Activate the virtual environment
source venv/bin/activate

# Install the dependencies
pip install -r requirements.txt

# Start the Celery worker
celery -A backend worker -l info &

# Start the Django server
python manage.py runserver
