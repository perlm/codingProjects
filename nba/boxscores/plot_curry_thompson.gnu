
set terminal pngcairo size 1000,500 noenhanced font ",18"
set output 'currythompson.png'

set border linewidth 3 back
set size square
unset key

set label 1 "hastydata.wordpress.com" at 0.5,0.9 font ",8" tc rgb "blue"

set xrange[0:1]
set xtics 0.25
set yrange[0:1]
set ytics 0.25

#set cbrange[0:50]
#set cbtics 10
#set palette defined ( 0 "white", 25 "blue", 50 "red" )

set multiplot layout 1,2
set xlabel "Curry Field Goal%"
set ylabel "Thompson Field Goal%"

set title "All Field Goals"
plot 'CurryThompson.data' u 1:3 w p pt 7 ps 1

set title "3pt Field Goals"
plot 'CurryThompson.data' u 2:4 w p pt 7 ps 1
unset multiplot
