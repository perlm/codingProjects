
set terminal pngcairo size 1000,500 noenhanced font ",16"
set output 'diff_histogram.png'

set border linewidth 3 back
set size square

set label 1 "hastydata.wordpress.com" at -5,0.0325 font ",12" tc rgb "blue"

set xrange[-50:50]
set xtics 25
set boxwidth 1

set key top left samplen 1

set xlabel "Point Differential"
set ylabel "Fraction"
plot 'histogram.data' u ($1-0.000):4 w boxes fs transparent solid 0.5 noborder title "5%", 'histogram.data' u ($1-0.000):6 w boxes fs transparent solid 0.5 noborder title "10%", 'histogram.data' u ($1-0.000):10 w boxes fs transparent solid 0.25 noborder title "20%", 'histogram.data' u ($1-0.000):14 w boxes fs transparent solid 0.25 noborder title "30%"
