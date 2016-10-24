
set terminal pngcairo size 1400,800 noenhanced font ",18"
set output 'modelCompare.png'

set border linewidth 3 back
set size square
unset key

#set label 1 "hastydata.wordpress.com" at 0.6,0.6 font ",8" tc rgb "blue"

set xrange[0:47]
set xtics 6 font ",14"
set yrange[-30:30]
set ytics 10

set multiplot layout 2,3
set xlabel "Minutes Elapsed"
set ylabel "Score Differential\n(Home-Away)"

set cbrange[0:1]
set palette defined ( 0 "blue", 0.5 "white", 1 "red" )

set title "Data"
plot 'data/hist' u 1:2:($4!=-1?$4:1/0) w p pt 5 ps 1 palette

set title "Logistic Regression Model"
plot 'data/logisticRegression.data' u 1:2:($4!=-1?$4:1/0) w point pt 5 ps 1 palette
set title "Logistic Regression Interaction Model"
plot 'data/logisticRegressionInteraction.data' u 2:3:($6!=-1?$6:1/0) w point pt 5 ps 1 palette
set title "Logistic Regression 2-nd Order Model"
plot 'data/logisticRegressionPolynomial2.data' u 2:3:($8!=-1?$8:1/0) w point pt 5 ps 1 palette
set title "Logistic Regression 3-rd Order Model"
plot 'data/logisticRegressionPolynomial3.data' u 2:3::($12!=-1?$12:1/0) w point pt 5 ps 1 palette
set title "Logistic Regression 4-th Order Model"
plot 'data/logisticRegressionPolynomial4.data' u 2:3::($17!=-1?$17:1/0) w point pt 5 ps 1 palette

unset multiplot

