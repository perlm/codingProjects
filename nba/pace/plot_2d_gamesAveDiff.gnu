
set terminal pngcairo size 600,500 noenhanced font ",18"
set output 'gamePaceDiff.png'

set border linewidth 3 back
set size square
unset key

set xlabel "Home Team Avg Pace"
set ylabel "Away Team Avg Pace"

set cbrange[-5:5]
set palette defined ( -5 "red", 0 "blue", 5 "green" )

set title "Difference between Avg and Actual Game Paces"
plot 'avg_2d_pace.data' u 2:1:($3-(($2+$1)/2.0)) w p pt 5 ps 3 palette

