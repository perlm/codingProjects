
#set terminal pngcairo size 1400,800 noenhanced font ",18"
#set output 'modelCompare.png'
set term canvas size 800,500 noenhanced fsize 24 mouse #jsdir "/usr/share/gnuplot/gnuplot/4.4/js/"
set output 'modelCompare.html'

set border linewidth 3 front
set size square
unset key

#set label 1 "hastydata.wordpress.com" at 0.6,0.6 font ",8" tc rgb "blue"

set xrange[0:48]
set xtics 12
set yrange[-30:30]
set ytics 10

#set multiplot layout 2,3
set xlabel "Minutes Elapsed"
set ylabel "Score Differential\n(Home-Away)"

set cbrange[0:1]
set palette defined ( 0 "blue", 0.5 "white", 1 "red" )

labeling(Prob) = sprintf("Prob= %f", column(Prob))

#set title "Probability of Home Team Win\nRaw Data"
#plot 'data/hist' u 1:2:((labeling(4))):($4!=-1?$4:1/0) w labels hypertext font ",32" point pt 5 ps 1 palette
#set title "Probability of Home Team Win\nLogistic Regression Model"
#plot 'data/logisticRegression.data' u 1:2:((labeling(4))):($4!=-1?$4:1/0) w labels hypertext font ",32" point pt 5 ps 1 palette
#set title "Probability of Home Team Win\nLogistic Regression Interaction Model"
#plot 'data/logisticRegressionInteraction.data' u 2:3:((labeling(6))):($6!=-1?$6:1/0) w labels hypertext font ",32" point pt 5 ps 1 palette
set title "Probability of Home Team Win\nLogistic Regression 2-nd Order Model"
plot 'data/logisticRegressionPolynomial2.data' u 2:3:((labeling(8))):($8!=-1?$8:1/0) w labels hypertext font ",32" point pt 5 ps 1 palette
#set title "Probability of Home Team Win\nLogistic Regression 3-rd Order Model"
#plot 'data/logisticRegressionPolynomial3.data' u 2:3:((labeling(12))):($12!=-1?$12:1/0) w labels hypertext font ",32" point pt 5 ps 1 palette
#set title "Probability of Home Team Win\nLogistic Regression 4-th Order Model"
#plot 'data/logisticRegressionPolynomial4.data' u 2:3:((labeling(17))):($17!=-1?$17:1/0) w labels hypertext font ",32" point pt 5 ps 1 palette

#unset multiplot

