#!/bin/bash

OUTPUT=`date +"%D, %H:%M:%S, "`
OUTPUT+=`/usr/bin/sensor`
echo $OUTPUT
