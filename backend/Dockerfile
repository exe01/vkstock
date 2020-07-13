FROM python:3.6

ENV PYTHONUNBUFFERED 1

WORKDIR /app
COPY ./ /app

RUN pip install -r requirements.txt

ENV DJANGO_MEDIA_ROOT '/app/media/'

CMD python manage.py runserver 0.0.0.0:8000
