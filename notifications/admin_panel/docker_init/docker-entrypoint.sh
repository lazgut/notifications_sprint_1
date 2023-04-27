#!/bin/bash

# Wait start DB server
echo "Wait start DB server"
docker_init/wait-for-it.sh postgres:5432

# Start server
echo "Starting server"
uwsgi --strict --ini /opt/app/uwsgi.ini