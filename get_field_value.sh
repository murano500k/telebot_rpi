#!/bin/bash
if [ -z $1 ]; then
  echo "Usage: get_field_value [1, 2]"
  exit 1
fi

function jsonval {
    temp=`echo $json | sed 's/\\\\\//\//g' | sed 's/[{}]//g' | awk -v k="text" '{n=split($0,a,","); for (i=1; i<=n; i++) print a[i]}' | sed 's/\"\:\"/\|/g' | sed 's/[\,]/ /g' | sed 's/\"//g' | grep -w $prop`
    echo ${temp##*|}
}
#https://api.thingspeak.com/channels/330894/feeds.json?results=1
json=`curl -s -X GET https://api.thingspeak.com/channels/330894/feeds.json?results=1`
prop="field$1"
result=`jsonval`
echo $result