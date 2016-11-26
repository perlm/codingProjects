
set terminal pngcairo size 500,500 enhanced
set output 'planets.png'

set size square
unset key
set ylabel "Number of Appearances"
set title "Planets and Jeopardy Responses"

set label 1 "hastydata.wordpress.com" at 3.75,105 font ",11" tc rgb "blue"

#set xrange[0:25]
set xtics font 'Arial,14' rotate by -60 font ",16"

plot 'planets.data' using 2:xticlabels(1) w boxes fs solid 0.25 border
