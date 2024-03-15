FROM python:3.11.8-slim

RUN mkdir backend
WORKDIR backend

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt update && apt -qy upgrade
RUN pip install --upgrade pip

ADD requirements.txt /backend/
RUN pip install --no-cache-dir -r ./requirements.txt
ADD . /backend/

RUN python manage.py collectstatic

#ADD .docker.env /backend/.env
ENV APP_NAME=Kapitoshka
CMD gunicorn config.wsgi:application -b 0.0.0.0:8000