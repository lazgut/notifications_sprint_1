# Wait start PostgreSQL
echo "Wait start PostgreSQL"
docker_init/wait-for-it.sh $DB_HOST:$DB_PORT -t $WAIT_TIMEOUT

echo "Starting server"
cd src
python main.py