#!/bin/bash
FILENAME=`date +"%d_%m_%y_%H-%M-%S"`
mv /home/artem/captures/image.jpg /home/artem/captures/image_$FILENAME.jpg 
if [ $? -ne 0 ]; then
  echo error
  exit 1
fi
