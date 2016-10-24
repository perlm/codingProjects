
set terminal pngcairo size 1000,500 noenhanced font ",16"
set output 'comeback.png'

set border linewidth 3 back
set size square

set label 1 "hastydata.wordpress.com" at 0.45,0.001 font ",12" tc rgb "blue"

set xrange[0:1]
set xtics 0.25
set yrange[0.:0.01]
set key top right

set xlabel "Fraction of Attempts which are 3pt"
set ylabel "Fraction of Comebacks"
plot 'data/comeBack.data' u 1:2 w lp pt 6 ps 3 lw 3 title "3FG%=33%", 'data/comeBack.data' u 1:3 w lp pt 8 ps 3 lw 3 lc 3 title "3FG%=40%"
