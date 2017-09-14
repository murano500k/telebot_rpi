#!/bin/bash
IP_PI=192.168.0.139
ssh pi@$IP_PI /home/pi/telebot_rpi/capture
mkdir -p ~/captures/in
rm -rf ~/captures/in/*
rsync pi@$IP_PI:/home/pi/captures/image.jpg ~/captures/in/image.jpg
FILENAME=`date +"%d_%m_%y_%H-%M-%S"`
mkdir -p ~/captures/vis
mkdir -p ~/captures/ndvi
cp ~/captures/in/image.jpg ~/captures/vis/image_$FILENAME.jpg 
~/projects/telebot_rpi/ndvi.sh
cp ~/captures/out/ndvi_image.jpg ~/captures/ndvi/ndvi_image_$FILENAME.jpg 
telegram-send --config channel.conf -i ~/captures/ndvi/ndvi_image_$FILENAME.jpg 



