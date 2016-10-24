
set terminal pngcairo size 600,600 noenhanced font ",16"
set output 'silhouette.png'

set border linewidth 3 back
set size square

#set label 1 "hastydata.wordpress.com" at 1.25,133 font ",12" tc rgb "blue"

#set multiplot layout 112

set xrange[0:8620]
set xtics 2500
#set yrange[0.25:1]
#set ytics 0.25
unset key

set palette defined ( 0 "red", 6 "blue", 12 "yellow", 18 "green" )

set xlabel "Food Index"
set ylabel "Silhouette Score"
set title "K-Means clustering of Foods based on Nutrition"

plot 'data/kmean_18_sort.data' u 0:3:2 w boxes fs transparent solid 0.5 noborder palette

