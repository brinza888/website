FROM python:3.8-alpine

ENV PYTHONDONTWRITEBYTECODE=1
EXPOSE 8000

WORKDIR /brinzabezrukoff

COPY . .

RUN pip install -r requirements.txt
RUN python manage.py db upgrade

ENTRYPOINT gunicorn -w 4 --bind 0.0.0.0:8000 wsgi:app
