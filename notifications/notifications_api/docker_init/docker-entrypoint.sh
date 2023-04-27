# Wait start RabbitMQ
echo "Wait start RabbitMQ"
docker_init/wait-for-it.sh $RABBIT_HOST:$RABBIT_PORT -t $WAIT_TIMEOUT

echo "Starting server"
cd src
gunicorn main:app --workers $UVICORN_WORKERS --worker-class uvicorn.workers.UvicornWorker --bind $UVICORN_HOST:$UVICORN_PORT