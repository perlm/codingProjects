
set terminal pngcairo size 500,500 noenhanced font ",16"
set output 'techChoice.png'

set border linewidth 3 back
set size square

set label 1 "hastydata.wordpress.com" at 0.5,0.35 font ",12" tc rgb "blue"

set multiplot layout 1,1

set xrange[0.25:1]
set xtics 0.25
set yrange[0.25:1]
set ytics 0.25
unset key

set xlabel "Common FT Shooter"
set ylabel "TF FT Shooter"
set title "FT Strategy"

plot 'data/switch.data' u 2:($3==0?$1:1/0) w p pt 7 ps 0.5, 'data/switch.data' u 2:($3==1?$1:1/0) w p pt 7 ps 0.5 lc 3, x lc rgb "dark-green" lw 3, x +0.05 lw 3 lc rgb "goldenrod"
