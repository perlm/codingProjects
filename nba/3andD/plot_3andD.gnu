
set terminal pngcairo size 600,500 noenhanced
set output '3andD.png'

set border linewidth 3 back
set size square
unset key
set title "Who were the best 3-And-D players in 2014-15?"

#set label 1 "hastydata.wordpress.com" at 1,52.5 font ",12" tc rgb "blue"

set xrange[110:95]

set xlabel "Defensive Rating"
set xtics 5
set ylabel "3pt%"
set ytics 0.05
plot '3andD.data' u 3:($1>1.5?$2:1/0):($1/3):($1) w circles fs transparent solid 0.5 border palette, '3andD.data' u 3:($1>1.5 && $2>0.45?$2:1/0):4 w labels font ",8" offset 0,-1.25, '3andD.data' u 3:($1>1.5 && $3<98?$2:1/0):4 w labels font ",8" offset 0,1.25, '3andD.data' u 3:($1>1.5 && $2>0.415 && $2<0.45?$2:1/0):4 w labels font ",8" offset 0,1.25

