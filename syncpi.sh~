#!/bin/bash
<<<<<<< HEAD
if [ -z $1 -o -z $2 ]; then
  echo "No param"
  echo '$1 - from dir, relative to /home/pi/, no / at the end'
  echo '$2 - to dir, relative to /home/artem/, no / at the end'
=======
if [ -z $1 || -z $2 ]; then
  echo "No param"
  echo "\$1 - from dir, relative to /home/pi/, no / at the end"
  echo "\$2 - to dir, relative to /home/artem/, no / at the end"
>>>>>>> 0866f3e112f9db771683bca2a7f942204ed9c9d4
  exit 1
fi
echo "syncing $1 to $2"
mkdir -p $2
IP_PI=192.168.0.139
rsync -rvl pi@$PI_IP:/home/pi/$1/ /home/artem/$2/
if [ $? -ne 0 ]; then
  echo error
  exit 1
fi
