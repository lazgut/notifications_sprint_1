# Wait start PostgreSQL
echo "Wait start PostgreSQL"
docker_init/wait-for-it.sh $DB_HOST:$DB_PORT -t $WAIT_TIMEOUT

# Wait start RabbitMQ
echo "Wait start RabbitMQ"
docker_init/wait-for-it.sh $RABBIT_HOST:$RABBIT_PORT -t $WAIT_TIMEOUT

# Wait start MailHog
echo "Wait start MailHog"
docker_init/wait-for-it.sh $EMAIL_HOST:$EMAIL_PORT -t $WAIT_TIMEOUT

echo "Starting server"
cd src
python main.py email