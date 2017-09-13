#!/bin/bash
if [ -z $1 ]; then
	echo "no parameter"
fi
rm -rf /home/artem/captures/in/*
cp $1 /home/artem/captures/in/
python processNGB.py /home/artem/captures/in/ /home/artem/captures/out/ -0.05 0.7 1
rsync
