#!/bin/bash
IP_PI=192.168.0.139
ssh pi@$IP_PI /home/pi/telebot_rpi/history.sh
~/telebot_rpi/syncpi.sh
~/telebot_rpi/copy_image.sh



