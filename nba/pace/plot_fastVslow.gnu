
set terminal pngcairo size 600,1000 noenhanced font ",18"
set output 'fastVslow.png'

set border linewidth 3 back
#set size square

set label 1 "hastydata.wordpress.com" at 86,0.14 font ",8" tc rgb "blue"

set multiplot layout 2,1

set title "Who controls Pace in the NBA?"

set xlabel "Game Pace"
set xtics 5
set xrange[85:105]
set ylabel "Frequency"
set ytics 0.04
set yrange [0:0.16]

set key

plot 'fastVslow.data' u 1:3 w boxes fs transparent solid 0.25 border lw 2 title "Slow-Slow", 'fastVslow.data' u 1:4 w boxes fs transparent solid 0.25 border lw 2 title "Fast-Fast", 'fastVslow.data' u 1:2 w boxes fs transparent solid 0.25 border lw 2 title "Fast-Slow"

set yrange [0:0.2]
set title "Can the Fastest teams change the pace?"
set key top left width 0 samplen 0
plot 'fastVslow.data' u 1:2 w boxes fs transparent solid 0.25 border lw 2 title "Fast-Slow",  'fastVslow.data' u 1:5 w boxes fs transparent solid 0.25 border lw 2 title "Very Fast-Slow"

unset multiplot
