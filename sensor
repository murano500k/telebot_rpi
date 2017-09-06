#!/usr/bin/env bash
RESULT=`/usr/local/bin/Adafruit_DHT 22 18`

#after
H=${RESULT##* }
H=${H##*=}
H=${H%%.*}

#before
T=${RESULT%% *}
T=${T##*=}
T=${T%%.*}

if [ "$1" == "h" ]; then
  echo $H
elif [ "$1" == "t" ]; then
  echo $T
else
  echo $RESULT
fi
