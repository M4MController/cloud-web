#!/bin/bash

if [[ $1 == "" ]]; then
  echo "Usage: ./update-app-remotely.sh <controller_ip> [<source directory>]";
  exit;
fi;

if [[ $2 == "" ]]; then
  source_dir = './frontend';
  git clone https://github.com/m4mcontroller/frontend $source_dir;
else
  source_dir=$2;
fi;

controller_host=$1;

cd $source_dir;

npm install;
MODE=lite npm run build -- --environment=production;

scp -r dist pi@"$controller_host":/tmp;
ssh pi@"$controller_host" 'sudo rm -rf /usr/html; sudo mv /tmp/dist /usr/html/;'

if [[ $2 == "" ]]; then
  rm -rf frontend;
fi;
