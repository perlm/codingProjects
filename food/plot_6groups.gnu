
set terminal pngcairo size 600,600 noenhanced font ",16"
set output '6FoodGroups.png'

set border linewidth 3 back
set size square

#set label 1 "hastydata.wordpress.com" at 1.25,133 font ",12" tc rgb "blue"

#set multiplot layout 112

set xrange[-3:7]
set xtics 2
set yrange[-5:5]
set ytics 2
unset key

set palette defined ( 0 "red", 2 "blue", 4 "black", 6 "green" )

set xlabel "PC 1"
set ylabel "PC 2"
set cblabel "Food Group"
set title "K-Means Clustering to 6 Food Groups"

plot 'data/kmean_out_pca10_6_sort.data' u 4:5:2 w p pt 7 ps 1 palette

