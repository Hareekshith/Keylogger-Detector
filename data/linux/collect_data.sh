#!/bin/sh
#collect_data.sh

#create a folder named samples
mkdir -p samples
#gets the required feed from the computer
for i in {1..10}
do
  sleep 5;
  ps -eo pid,comm,%cpu,%mem --sort=-%cpu --no-headers | while read pid comm cpu mem; do echo "${pid}|${comm}|${cpu}|${mem}" >> "samples/ldata$i.csv"
done
done
