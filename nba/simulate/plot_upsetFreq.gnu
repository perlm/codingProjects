
set terminal pngcairo size 1000,500 noenhanced font ",16"
set output 'upset.png'

set border linewidth 3 back
set size square

set label 1 "hastydata.wordpress.com" at 0.23,0.37 font ",12" tc rgb "blue"

set xrange[0:0.5]
set xtics 0.1
set yrange[0.1:0.45]
set key top right

set xlabel "Fraction of Attempts which are 3pt"
set ylabel "Fraction of Upset Victories"
plot 'results.data' u 1:2 w lp pt 5 ps 3 lw 3 title "Good v Bad", 'results.data' u 1:3 w lp pt 7 ps 3 lw 3 lc 3 title "Good v Average" #, 'results.data' u 1:4 w lp pt 9 ps 3 lw 3 lc 4 title "In v Out"
