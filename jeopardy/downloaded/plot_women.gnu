
set terminal pngcairo size 500,500 noenhanced
set output 'women.png'

set border linewidth 3 back
#set size square
unset key
set ylabel "Number of Appearances"
set title "Most Frequent Women on Jeopardy

set label 1 "hastydata.wordpress.com" at 10,100 font ",12" tc rgb "blue"

set xtics rotate by -60 font ',12'
set xrange[0:25]
set yrange[0:]

plot 'mostFrequentWomen.data' using 2:xticlabels(1) w boxes fs solid 0.25 border lw 2 
