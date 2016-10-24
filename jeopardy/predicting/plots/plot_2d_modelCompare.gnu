
set terminal pngcairo size 1200,400 noenhanced font ",16"
set output 'modelCompare.png'

set border linewidth 3 back
set size square
unset key

#set label 1 "hastydata.wordpress.com" at 0.6,0.6 font ",8" tc rgb "blue"

set multiplot layout 1,3

set xlabel "Previous Winnings ($)"
set ylabel "Probability of Repeat Champ"
set yrange[0:1]
set xrange[0:50000]
set xtics 25000
plot 'data/ave.data' w p pt 7 ps 2

set xlabel "Number of Previous Victories"
set xrange[0:10]
set xtics 2
plot 'data/aveNumberWins.data' w p pt 7 ps 2

set xrange[1:10]
set xtics 2
set xlabel "Previous Victories"

set yrange[0:100000]
set ytics 25000
set ylabel "Total Winnings"

set cbrange[0.25:0.75]
set cbtics 0.25
set palette defined ( 0.25 "red", 0.5 "blue", 0.75 "green" )

plot 'data/logisticRegressionLinear.data' u ($1+1.89773038009):(1000*($2+31.7529075745)):3 w point pt 5 ps 2 palette
#plot 'data/logisticRegressionPolynomial3.data' u ($2+1.89773038009):(1000*($3+31.7529075745)):11 w point pt 5 ps 3 palette

unset multiplot

