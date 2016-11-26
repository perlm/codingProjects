
set term postscript eps enhanced color size 10cm,10cm "Arial" 24
set output 'mostFreq.jpg'

set size square
unset key
set ylabel "Number of Appearances"
set title "Most Frequent Jeopardy Responses"

set label 1 "hastydata.wordpress.com" at 7,270 font ",24" tc rgb "blue"

set xrange[0:25]
set xtics font 'Arial,14' rotate by -60 font ",16"

plot 'mostFrequent.data' using 2:xticlabels(1) w p pt 7 ps 3
