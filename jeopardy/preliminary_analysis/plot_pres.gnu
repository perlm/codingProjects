
set terminal pngcairo size 1500,500 noenhanced
set output 'presidents.png'

#set size square
unset key
set ylabel "Number of Appearances"
set title "American Presidents on Jeopardy"
set yrange[0:]

set label 1 "hastydata.wordpress.com" at 35,205 font ",14" tc rgb "blue"

set xtics rotate by -60 font ',12'

plot 'presidents.data' using 2:xticlabels(1) w boxes fs solid 0.25 border
