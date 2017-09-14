#!/bin/bash

if [ -z $1 -o -z $2 ]; then
  echo "No param"
  echo '$1 - from dir, relative to /home/pi/, no / at the end'
  echo '$2 - to dir, relative to /home/artem/, no / at the end'
  exit 1
fi
echo "syncing $1 to $2"
mkdir -p $2
IP_PI=192.168.0.139
rsync -rvl pi@$IP_PI:/home/pi/$1/ /home/artem/$2/
if [ $? -ne 0 ]; then
  echo error
  exit 1
fi
