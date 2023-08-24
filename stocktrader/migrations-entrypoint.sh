#! /bin/bash
poetry run python manage.py migrate --database=master
poetry run python manage.py createsuperuser --noinput --database=master