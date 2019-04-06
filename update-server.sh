#!/bin/bash

if ! type "nginx" > /dev/null; then 
	apt update;
	apt install nginx -y;
fi;

cp -f nginx.conf /etc/nginx/nginx.conf;
service nginx reload;
