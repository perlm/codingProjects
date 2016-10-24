
set terminal pngcairo size 500,500 noenhanced font ",18"
set output 'shootingRebounds.png'

set border linewidth 3 back
set size square
unset key

set label 1 "hastydata.wordpress.com" at 50,65 font ",8" tc rgb "blue"

set xtics 10
set xrange[25:70]
set ytics 20
set yrange[20:70]

#set cbrange[0:50]
#set cbtics 10
#set palette defined ( 0 "white", 25 "blue", 50 "red" )

set multiplot layout 1,1
set xlabel "Opponent Field Goal%"
set ylabel "Number of Rebounds"

plot 'shootingRebounds.data' u 2:1 w p pt 7 ps 0.5, 'shootingRebounds.data' u 4:3 w p pt 7 ps 0.5 lc 1
unset multiplot
