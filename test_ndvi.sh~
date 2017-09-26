#!/bin/bash -e
if [ -z $1 -o -z $2 ]; then
 exit 1
fi
mkdir -p /home/artem/captures/test_ndvi/
python /home/artem/projects/telebot_rpi/processNGB.py /home/artem/captures/in/ /home/artem/captures/out/ $1 $2 0
cp /home/artem/captures/out/ndvi_image.jpg /home/artem/captures/test_ndvi/ndvi_image_$1-$2.jpg
echo /home/artem/captures/test_ndvi/ndvi_image_$1-$2.jpg
