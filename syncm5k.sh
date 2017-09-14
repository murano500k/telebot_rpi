#!/bin/bash
IP_HOME=192.168.0.108

if [ -z $1 ]; then
  echo "No param"
  echo '$1 - from dir, relative to /home/pi/, no / at the end'
  echo '$2 - to dir, relative to /home/artem/, no / at the end'
  exit 1
fi
FROM_DIR=$1
if [ -z $2 ]; then
  TO_DIR=$FROM_DIR
else
  TO_DIR=$2
fi

echo "syncing $FROM_DIR to $TO_DIR"
mkdir -p $TO_DIR
rsync -rvl artem@$IP_HOME:/home/artem/$FROM_DIR/ ~/$TO_DIR/
if [ $? -ne 0 ]; then
  echo error
  exit 1
fi

