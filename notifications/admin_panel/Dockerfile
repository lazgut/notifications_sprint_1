FROM python:3.10

WORKDIR /opt/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV UWSGI_PROCESSES 1
ENV UWSGI_THREADS 16
ENV UWSGI_HARAKIRI 240
ENV DJANGO_SETTINGS_MODULE 'config.settings'
ENV PYTHONPATH '/opt/app'

COPY requirements.txt requirements.txt

RUN apt-get update -y \
	 && apt-get install gettext -y \
	 &&	pip install --upgrade pip \
     && pip install -r requirements.txt --no-cache-dir

COPY src/uwsgi/uwsgi.ini uwsgi.ini
COPY ./docker_init ./docker_init
COPY ./src .

EXPOSE 8000

ENTRYPOINT [ "bash", "/opt/app/docker_init/docker-entrypoint.sh" ]
