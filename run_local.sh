#!/usr/bin/env bash

MYSQL_ENV_FILE="mysql-prod.env"

# only need to setup virtual machine if running on windows or mac osx
if [ "$(uname -s)" != 'Linux' ] 
then
    echo "Not running on Linux, setting up virtualbox"
    #create local virtual machine if it doesn't exist
    docker-machine create --driver virtualbox default
    docker-machine start default

    # setup environment
    eval "$(docker-machine env default)"

    # print ip
    printf "\nWill run at this ip: "
    docker-machine ip default
    printf "\n"
fi

# stop on any errors after this
set -e

# check if mysql .env file exists
if [ ! -f "${MYSQL_ENV_FILE}" ]
then
    echo "Enter MySQL credentials:"
    read -p "MySQL Username: " mysql_username
    read -p "MySQL Password: " mysql_password
    echo "MYSQL_USER=${mysql_username}" >> mysql-prod.env
    echo "MYSQL_PASSWORD=${mysql_password}" >> mysql-prod.env
    echo "MYSQL_ROOT_PASSWORD=${mysql_password}" >> mysql-prod.env
fi 

# stop already running containers
printf "\nStopping old containers\n"
docker stop $(docker ps -a -q) || true
docker rm $(docker ps -a -q) || true
#docker rmi $(docker images -q) || true



# run the app
docker-compose up

#create database
# docker-compose run -d --rm --no-deps app python app.py create_db
#
