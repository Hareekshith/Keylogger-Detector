#!/bin/sh
#collect_data.sh

#clears previous data
> ldata.csv

#gets the required feed from the computer
ps -eo pid,comm,%cpu,%mem --sort=-%cpu --no-headers | while read pid comm cpu mem; do echo "${pid}|${comm}|${cpu}|${mem}" >> ldata.csv
done
