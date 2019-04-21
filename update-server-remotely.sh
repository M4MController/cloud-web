#!/bin/bash

if [[ $1 == "" ]]; then
  echo "Usage: ./update-server-remotely.sh <controller_ip>";
  exit;
fi;

controller_host=$1;

scp -r update-server.sh nginx.conf sensor.example pi@"$controller_host":/tmp/;
ssh pi@"$controller_host" 'cd /tmp && sudo ./update-server.sh';
