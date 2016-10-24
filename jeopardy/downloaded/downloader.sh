#!/bin/bash

#simple script. Goes through numerically, downloading file.
#then erases it if it doesn't contain appropriate data...
for i in `seq 1 5000`;
do
	if [ ! -f "showgame.php?game_id="$i ]
	then
		wget "http://www.j-archive.com/showgame.php?game_id="$i
	fi

	lines=$(wc "showgame.php?game_id="$i |awk '{print $1'})
	if [ 50 -gt $lines ]
	then 
		echo $i
		rm "showgame.php?game_id="$i
	fi

done
