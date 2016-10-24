
set terminal pngcairo size 1000,500 noenhanced
set output 'catchShoot.png'

set border linewidth 3 back
#set size square
unset key

set ylabel "Number of Open 3s per Game (defender >4ft)"

set label 1 "hastydata.wordpress.com" at 41,25 font ",10" tc rgb "blue"

set multiplot layout 1,2
set xtics 5

set xrange[40:55]

set title "Shooting Forwards and Open 3s"
set xlabel "Forward Catch-and-Shoot eFG%"
plot 'summary_forwards.data' u 2:7:3 w p pt 5 ps 3 palette

set label 1 "hastydata.wordpress.com" at 36,25 font ",10" tc rgb "blue"
set xrange[35:60]
set title "Shooting Centers and Open 3s"
set xlabel "Centers Catch-and-Shoot eFG"
plot 'summary_centers.data' u 2:7:3 w p pt 5 ps 3 palette

unset multiplot
