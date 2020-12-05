#!/bin/sh
flask db upgrade
exec gunicorn -w 4 -b :8000 --error-logfile - --access-logfile - wsgi:app
