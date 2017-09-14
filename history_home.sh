#!/bin/bash
IP_PI=192.168.0.139
ssh pi@$IP_PI /home/pi/telebot_rpi/history.sh
/home/pi/telebot_rpi/syncpi.sh
/home/pi/telebot_rpi/copy_image.sh



