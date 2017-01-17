#!/usr/bin/env bash

DOCKERHUB_USER="hallofswe"
APP_NAME="dudecarryme"
MYSQL_ENV_FILE="mysql-prod.env"

# stop on any errors
set -e

source source_prod.sh

if [[ $* != *-s* ]];
then
    #login to docker-hub
    printf "\n\nEnter docker-hub credentials:\n"
    docker login

    # build images and push to docker-hub
    docker build -t ${DOCKERHUB_USER}/${APP_NAME}_app app
    docker push ${DOCKERHUB_USER}/${APP_NAME}_app
    docker build -t ${DOCKERHUB_USER}/${APP_NAME}_lb lb
    docker push ${DOCKERHUB_USER}/${APP_NAME}_lb
    docker build -t ${DOCKERHUB_USER}/${APP_NAME}_db db
    docker push ${DOCKERHUB_USER}/${APP_NAME}_db
fi

# check if mysql .env file exists
if [ ! -f "${MYSQL_ENV_FILE}" ]
then
    echo "Enter MySQL credentials:"
    read -p "MySQL Username: " mysql_username
    read -s -p "MySQL Password: " mysql_password
    echo "MYSQL_USER=${mysql_username}" >> mysql-prod.env
    echo "MYSQL_PASSWORD=${mysql_password}" >> mysql-prod.env
    echo "MYSQL_ROOT_PASSWORD=${mysql_password}" >> mysql-prod.env
fi 



echo "Stopping and deleting old containers:"
docker stop $(docker ps -a) || true
docker rm $(docker ps -a -q) || true
docker rmi $(docker images -q) || true

# start up server
docker-compose --file docker-compose-prod.yml up -d

echo "Giving database time to to start up"
sleep 30

echo "Running create_db"
docker-compose --file docker-compose-prod.yml run -d --rm --no-deps app python app.py create_db
sleep 30

echo "Running populate"
docker-compose --file docker-compose-prod.yml run -d --rm --no-deps app python app.py populate

sleep 60

# print ip and port
echo "ip address:"
docker port ${APP_NAME}_lb 80 
