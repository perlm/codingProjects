
set terminal pngcairo size 1000,500 noenhanced font ",16"
set output 'techs_histogram.png'

set border linewidth 3 back
set size square

set label 1 "hastydata.wordpress.com" at 0.005,0.4 font ",14" tc rgb "blue"

set xrange[0:0.015]
set xtics 0.005
set boxwidth 0.001

set xlabel "Technicals per Minute"
set ylabel "Fraction"
plot 'histogram.data' u ($1-0.000):2 w boxes fs transparent solid 0.25 border lw 2 title "US", 'histogram.data' u ($1+0.000):3 w boxes fs transparent solid 0.25 border lw 2 title "International"
