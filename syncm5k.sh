#!/bin/bash
if [ -z $1 || -z $2 ]; then
  echo "No param"
  echo "\$1 - from dir, relative to /home/artem"
  echo "\$2 - to dir, absolute path"
  exit 1
fi
HOME_IP=192.168.0.108
echo "syncing $1 to $2"
mkdir -p $2
rsync -rvl artem@$HOME_IP:/home/artem/$1 $2
if [ $? -ne 0 ]; then
  echo error
  exit 1
fi

