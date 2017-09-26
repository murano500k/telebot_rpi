#!/bin/bash
ffmpeg -r 24 -pattern_type glob -i '/home/artem/captures/ndvi/*.jpg'  -c:v libx264 -preset slow -profile:v high -crf 18 -coder 1 -pix_fmt yuv420p -movflags +faststart -g 30 -bf 2 -c:a aac -b:a 384k -profile:a aac_low /home/artem/captures/timelapse_ndvi_v1.mp4

#ffmpeg -i '/home/artem/captures/ndvi/*.jpg' -c:v libx264 -preset slow -profile:v high -crf 18 -coder 1 -pix_fmt yuv420p -movflags +faststart -g 30 -bf 2 -c:a aac -b:a 384k -profile:a aac_low /home/artem/captures/timelapse_ndvi_v1.mp4
#python /home/artem/projects/telebot_rpi/processNGB.py /home/artem/captures/in/ /home/artem/captures/out/ -0.35 1 0
