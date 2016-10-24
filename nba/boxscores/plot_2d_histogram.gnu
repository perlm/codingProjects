
set terminal pngcairo size 1000,500 noenhanced font ",18"
set output 'histogram_2d.png'

set border linewidth 3 back
set size square
unset key

#set label 1 "hastydata.wordpress.com" at 0.6,0.6 font ",8" tc rgb "blue"

set xrange[0:1]
set xtics 0.25
set yrange[0:1]
set ytics 0.25

set cbrange[0:50]
set cbtics 10
set palette defined ( 0 "white", 25 "blue", 50 "red" )

set multiplot layout 1,2
set xlabel "PG Field Goal%"
set ylabel "SG Field Goal%"

set title "All Field Goals"
plot 'pg_and_sg.hist.05' u 1:2:3 w p pt 5 ps 3 palette

#set cbrange[0:250]
#set cbtics 50
#set palette defined ( 0 "white", 125 "blue", 250 "red" )

set title "3pt Field Goals"
plot 'pg_and_sg.hist.05' u 1:2:4 w p pt 5 ps 3 palette
unset multiplot
