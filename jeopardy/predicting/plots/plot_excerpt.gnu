
set terminal pngcairo size 600,400 noenhanced font ",16"
set output 'exc.png'

set border linewidth 3 back
set size square
unset key


set xrange[1:10]
set xtics 2
set xlabel "Previous Victories"

set yrange[0:100000]
set ytics 25000
set ylabel "Total Winnings"

set cbrange[0.25:0.75]
set cbtics 0.25
set palette defined ( 0.25 "red", 0.5 "blue", 0.75 "green" )
set cblabel "Probability of Champ Repeat"

plot 'data/logisticRegressionLinear.data' u ($1+1.89773038009):(1000*($2+31.7529075745)):3 w point pt 5 ps 2 palette
#plot 'data/logisticRegressionPolynomial3.data' u ($2+1.89773038009):(1000*($3+31.7529075745)):11 w point pt 5 ps 3 palette


