
set terminal pngcairo size 1000,1000 noenhanced font ",16"
set output 'scatter.png'

set border linewidth 3 back
set size square

set label 1 "hastydata.wordpress.com" at 0.5,0.35 font ",12" tc rgb "blue"

set multiplot layout 2,2

set xrange[0.25:1]
set xtics 0.25
set yrange[0.25:1]
set ytics 0.25
unset key

f1(x) = a1+x
fit f1(x) 'data/freeThrows.data' u ($2+$4+$6)/($3+$5+$7):($5>50?$2/$3:1/0) via a1
f2(x) = a2+x
fit f2(x) 'data/freeThrows.data' u ($2+$4+$6)/($3+$5+$7):($5>50?$4/$5:1/0) via a2
f3(x) = a3+x
fit f3(x) 'data/freeThrows.data' u ($2+$4+$6)/($3+$5+$7):($7>5?$6/$7:1/0) via a3

set xlabel "First FT%"
set ylabel "Second FT%"
set title "FT% on First vs Second Attempts"
plot 'data/freeThrows.data' u ($2/$3):($5>50?$4/$5:1/0) w p pt 7 lc 1 ps 1 notitle, x w l lw 4 lc 3 notitle

set title "Ave FT% vs First Attempts"
set xlabel "Ave FT%"
set ylabel "First FT%"
plot 'data/freeThrows.data' u ($2+$4+$6)/($3+$5+$7):($3>50?$2/$3:1/0) w p pt 7 lc 1 ps 1 notitle, x w l lw 4 lc 3 notitle, f1(x) w l lw 4 lc rgb "goldenrod" notitle

set title "Ave FT% vs Second Attempts"
set ylabel "Second FT%"
plot 'data/freeThrows.data' u ($2+$4+$6)/($3+$5+$7):($5>50?$4/$5:1/0) w p pt 7 lc 1 ps 1 notitle, x w l lw 4 lc 3 notitle, f2(x) w l lw 4 lc rgb "goldenrod" notitle

set ylabel "Third FT%"
set title "Ave FT% vs Third Attempts"
plot 'data/freeThrows.data' u ($2+$4+$6)/($3+$5+$7):($7>5?$6/$7:1/0) w p pt 7 lc 1 ps 1 notitle, x w l lw 4 lc 3 notitle, f3(x) w l lw 4 lc rgb "goldenrod" notitle

print a1,a2, a3
