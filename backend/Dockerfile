FROM python:3.6

ENV PYTHONUNBUFFERED 1

WORKDIR /backend
COPY ./ /backend

RUN pip install -r requirements.txt
RUN pip install git+git://github.com/arsensokolov/djantimat.git#egg=djantimat


ENV DJANGO_MEDIA_ROOT '/backend/media/'

CMD python manage.py runserver 0.0.0.0:8000
