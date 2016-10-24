
set terminal pngcairo size 600,400 noenhanced
set output 'flyingaway.png'

set border linewidth 3 back
#set size square
set key top right
set title "Distribution of Commercial Flight Distances"

set multiplot layout 1,1

set ylabel "Number of Flights"
set label 1 "hastydata.wordpress.com" at 4000,1800 font ",12" tc rgb "blue"
set xrange[0:8500]
set xlabel "Distance (miles)"
set ylabel "Number of Flights"

plot 'flightLengths.data' using 1:2 w boxes fs transparent solid 0.1 border lw 1 title "All", 'flightLengths.data' using 1:6 w boxes fs transparent solid 0.1 border lw 1 title "Europe", 'flightLengths.data' using 1:3 w boxes fs transparent solid 0.1 border lw 1 title "US", 'flightLengths.data' using 1:4 w boxes fs transparent solid 0.1 border lw 1 title "China", 'flightLengths.data' using 1:5 w boxes fs transparent solid 0.1 border lw 1 title "Brazil"

unset multiplot
#flightLengths.data

