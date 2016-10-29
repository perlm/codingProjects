#!/bin/bash

SAVEIFS=$IFS
IFS=$(echo -en "\n\b")
a=1
for f in *zip
do
	unzip $f
	mv 374657178_T_ONTIME.csv file_$a.csv
	a=$((a+1))
done

