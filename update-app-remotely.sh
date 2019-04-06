#!/bin/bash

if [[ $1 == "" ]]; then
  echo "Usage: ./update-app-remotely.sh <controller_ip>";
  exit;
fi;

controller_host=$1;
 
git clone https://github.com/m4mcontroller/frontend;
cd frontend;

npm install;
MODE=lite npm run build -- --environment=production;

scp -r dist pi@"$controller_host":/tmp;
ssh pi@"$controller_host" 'sudo rm -rf /usr/html; sudo mv /tmp/dist /usr/html/;'

cd ..;
rm -rf frontend;
