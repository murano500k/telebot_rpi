#!/bin/bash

OUTPUT=`date +"%D, %H:%M:%S, "`
OUTPUT+=`/usr/bin/sensor`
echo $OUTPUT
echo $OUTPUT >> /home/pi/history.log
/home/pi/telebot_rpi/capture
/home/pi/telebot_rpi/sendphoto


