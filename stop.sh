#!/bin/bash

# Find the process IDs of the Django server and Celery worker
django_pid=$(lsof -ti :8000)
celery_pid=$(ps aux | grep 'celery -A backend' | grep -v grep | awk '{print $2}')

# Check if the Django server process ID exists and terminate the server
if [[ -n $django_pid ]]; then
    kill $django_pid
fi

# Check if the Celery worker process ID exists and terminate the worker
if [[ -n $celery_pid ]]; then
    kill $celery_pid
fi
