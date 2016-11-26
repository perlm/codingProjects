
set terminal pngcairo size 500,500 noenhanced
set output 'henry.png'

set size square
unset key
set ylabel "Number of Appearances"
set title "Wives of Henry VIII on Jeopardy"

set label 1 "hastydata.wordpress.com" at 2,35 font ",12" tc rgb "blue"

set xtics rotate by -60 font ',13'

plot 'henry.data' using 2:xticlabels(1) w boxes fs solid 0.25 border
