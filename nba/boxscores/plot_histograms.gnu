
set terminal pngcairo size 750,500 noenhanced font ",16"
set output 'histogram.png'

set border linewidth 3 back
set size square

set label 1 "hastydata.wordpress.com" at 50,0.225 font ",10" tc rgb "blue"

set xrange[0:100]
set xtics 25
#set boxwidth 1

set key top left samplen 1

set title "GSW FG% 14-15"

set xlabel "Field Goal Percentage"
set ylabel "Fraction"
plot 'histogram.data' u ($1-0.000):2:(3) w boxes fs transparent solid 0.75 noborder title "All FG", 'histogram.data' u ($1-0.000):3:(3) w boxes fs transparent solid 0.5 noborder title "3pt"
