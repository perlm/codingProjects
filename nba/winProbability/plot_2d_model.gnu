
set terminal pngcairo size 1400,400 noenhanced font ",16"
set output 'modelSummary1.png'

set border linewidth 3 back
set size square
unset key

set xrange[0:47]
set xtics 6 font ",14"
set yrange[-30:30]
set ytics 10

set multiplot layout 1,3
set xlabel "Minutes Elapsed"
set ylabel "Score Differential\n(Home-Away)"

set cbrange[0:500]
set palette defined ( 0 "white", 250 "dark-green", 500 "black" )
set title "Number of Occurences in Dataset"
plot 'data/hist' u 1:2:($3!=0?$3:1/0) w p pt 5 ps 2 palette

set cbrange[0:1]
set palette defined ( 0 "blue", 0.5 "white", 1 "red" )

set title "Home Team Win Probability - Data"
plot 'data/hist' u 1:2:($4!=-1?$4:1/0) w p pt 5 ps 1 palette

set title "Home Team Win Probability - Model"
plot 'data/logisticRegressionPolynomial2.data' u 2:3:($8!=-1?$8:1/0) w point pt 5 ps 1 palette
unset multiplot

set terminal pngcairo size 1000,350 noenhanced font ",14"
set output 'modelSummary2.png'

set multiplot layout 1,2
set yrange[-5:35]
set ytics 10 nomirror
set y2range[0:1]
set y2tics 0.25

set ylabel "Score Differential\n(Home-Away)" textcolor rgb "blue"
set y2label "Home Team Win Probability" textcolor rgb "red"

set title "Random Game"
plot 'data/game_0.data' u 1:2 w lp pt 5 lc 3 lw 3, 'data/game_0.data' u 1:3 axes x1y2 w lp pt 7 lc 1 lw 3 ps 1

set title "Most Unlikely Game"
plot 'data/game_152400.data' u 1:2 w lp pt 5 lc 3 lw 3, 'data/game_152400.data' u 1:3 axes x1y2 w lp pt 7 lc 1 lw 3 ps 1


unset multiplot

