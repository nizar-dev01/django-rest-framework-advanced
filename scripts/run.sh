#!/bin/sh

set -e # It will contain the entire script a single scope of failure, namely if any one line fails, it will be taken as the failure of the entire script

python manage.py wait_for_db
python manage.py collectstatic --noinput
python manage.py migrate

uwsgi --socket :9000 --workers 4 --master --enable-threads --module app.wsgi