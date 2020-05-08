# !/bin/bash

sudo docker-compose stop
sudo docker-compose rm
sudo docker-compose build --no-cache
sudo docker-compose up -d
