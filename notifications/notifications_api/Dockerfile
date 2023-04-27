FROM python:3.10

WORKDIR /opt/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH '/opt/app'

COPY requirements.txt requirements.txt

RUN apt-get update -y \
	 && apt-get install gettext -y \
	 &&	pip install --upgrade pip \
     && pip install -r requirements.txt --no-cache-dir

COPY ./docker_init ./docker_init
COPY ./src .

EXPOSE 8000

ENTRYPOINT [ "bash", "/opt/app/docker_init/docker-entrypoint.sh" ]