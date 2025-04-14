#!/bin/sh
#collect_data.sh

#create a folder named samples and csamples
mkdir -p samples
mkdir -p csamples
#gets the required feed from the computer
for i in $(seq 1 9);
do
  sleep 5;
  ps -eo pid,comm,%cpu,%mem --sort=-%cpu --no-headers | while read pid comm cpu mem; 
  do
  #Returns the path of the given program
  p=$(readlink -f "/proc/$pid/exe" 2>/dev/null)
  #Checks if the file running is either in log, dat or txt format
  ai=0
  if lsof -p "$pid" 2>/dev/null | grep -E '\.(txt|dat|log)$' > /dev/null; then
    ai=1;
  fi
  echo "${pid}|${comm}|${cpu}|${mem}|${p}|${ai}" >> samples/ldata$i.csv
  done
done
