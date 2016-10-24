
set terminal pngcairo size 1000,500 noenhanced font ",18"
set output 'histogram_2d.png'

set border linewidth 3 
set size square
unset key

#set label 1 "hastydata.wordpress.com" at 0.6,0.6 font ",8" tc rgb "blue"

set xrange[0:48]
set xtics 12
set yrange[-50:50]
set ytics 25

#set cbrange[0:50]
#set cbtics 10
#set palette defined ( 0 "white", 25 "blue", 50 "red" )

set multiplot layout 1,2
set xlabel "Minutes Elapsed"
set ylabel "Score Differential (Home-Away)"

set cbrange[0:500]
set palette defined ( 0 "white", 250 "dark-green", 500 "black" )
set title "Number of Occurences"
plot 'data/hist' u 1:2:($3!=0?$3:1/0) w p pt 5 ps 2 palette

set cbrange[0:1]
set palette defined ( 0 "blue", 0.5 "white", 1 "red" )
set title "Probability of Home Team Win"
plot 'data/hist' u 1:2:($4!=-1?$4:1/0) w p pt 5 ps 2 palette
unset multiplot

