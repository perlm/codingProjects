
set terminal pngcairo size 1200,1500 noenhanced font ",16"
set output 'heightParity.png'

set border linewidth 3 back
set size square

#set label 1 "hastydata.wordpress.com" at 1.25,133 font ",12" tc rgb "blue"

#set label 2 "GSW" at 1.25,91 font ",12" tc rgb "dark-green"
#set label 3 "CLE" at 1.25,112 font ",12" tc rgb "dark-green"

set multiplot layout 3,2

#set xrange[1:5]
set xtics 1
#set yrange[0.25:1]
#set ytics 0.25
unset key

set xlabel "Lineup Height RMSD (inches)"
#set title "Height parity does not correlate with defense"

#plot 'data/lineupHeight.data' u 1:4 w p pt 7 ps 1 notitle, 'data/lineupHeight.data' u 1:($1<2?$4:1/0) w p pt 7 ps 1 lc rgb "dark-green" notitle

set ylabel "Opposing eFG%"
plot 'data/lineupHeightStats.data' u 2:5 w p pt 7 ps 1 notitle
set ylabel "Opposing TO Fraction"
plot 'data/lineupHeightStats.data' u 2:6 w p pt 7 ps 1 notitle
set ylabel "Opposing Offensive Rebound Fraction"
plot 'data/lineupHeightStats.data' u 2:7 w p pt 7 ps 1 notitle
set ylabel "Opposing Second Chance Pts per 100 Pos"
plot 'data/lineupHeightStats.data' u 2:8 w p pt 7 ps 1 notitle
set ylabel "Opposing Fastbreak Pts per 100 Pos"
plot 'data/lineupHeightStats.data' u 2:9 w p pt 7 ps 1 notitle
set ylabel "Opposing Pts in the Paint per 100 Pos"
plot 'data/lineupHeightStats.data' u 2:10 w p pt 7 ps 1 notitle
