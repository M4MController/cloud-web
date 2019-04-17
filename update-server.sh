#!/bin/bash

if ! type "nginx" > /dev/null; then 
	apt update;
	apt install nginx -y;
fi;

cp -f nginx.conf /etc/nginx/nginx.conf;

mkdir -p /usr/api;
cp -n sensor.example /usr/api/sensor;

service nginx reload;
