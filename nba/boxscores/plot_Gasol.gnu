
set terminal pngcairo size 600,500 noenhanced font ",18"
set output 'Gasol.png'

set border linewidth 3 back
#set size square
unset key

set label 1 "hastydata.wordpress.com" at screen 0.25,0.75 font ",12" tc rgb "blue"

set timefmt '"%B %d, %Y"'
set xdata time
set format x "%B"
set xtics rotate by -60 font ",12"

set ylabel "# of Gasols/# NBA Games"

plot './Gasols.data' u 1:($3/$2) w p pt 7 ps 2

unset multiplot
