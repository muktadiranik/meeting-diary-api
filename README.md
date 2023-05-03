# meeting-diary-api

meeting-diary-api

## create .env

    touch .env

## copy from .env.example to .env

    cp .env.example .env

1. create postgres database and provide its credentials in .env
2. provide your preferred SMTP server credentials in .env
3. provide redis credentials in .env

## install virtual environment

    pip install virtualenv

## setup virtual environment

    virtualenv venv

## activate virtual environment

    source venv/bin/activate

## change directory to backend

    cd backend

## install dependencies

    pip install -r requirements.txt

## migrate database

    python manage.py migrate

## create superuser

    python manage.py createsuperuser

## runserver

    python manage runserver

## open another terminal and activate virtual environment to run celery worker

    source venv/bin/activate

## change directory to backend

    cd backend

## run celery worker to send emails

    celery -A backend worker -l INFO
