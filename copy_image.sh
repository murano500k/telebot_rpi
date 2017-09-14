#!/bin/bash
FILENAME=`date +"%d_%m_%y_%H-%M-%S"`
mkdir -p /home/artem/captures/all
cp /home/artem/captures/image.jpg /home/artem/captures/all/image_$FILENAME.jpg 
cp /home/artem/captures/ndvi_image.jpg /home/artem/captures/all/ndvi_image_$FILENAME.jpg 
if [ $? -ne 0 ]; then
  echo error
  exit 1
fi
