#!/bin/sh
set -e

echo "Deploying application ..."

    # Update codebase
    git fetch origin main
    git reset --hard origin/main

    # Install dependencies based on lock file
    python -m pip install --upgrade pip
    pip install -r requirements.txt

    # Migrate database
    python manage.py collectstatic --clear --noinput
    python manage.py makemigrations
    python manage.py migrate


# Exit maintenance mode
systemctl restart wellhouse
systemctl restart nginx

echo "Application deployed!"

chmod u+x deploy.sh
