
set terminal pngcairo size 600,500 noenhanced font ",18"
set output 'gamePace.png'

set border linewidth 3 back
set size square
unset key

set xlabel "Home Team Avg Pace"
set ylabel "Away Team Avg Pace"

set cbrange[85:105]
set palette defined ( 85 "red", 95 "blue", 105 "green" )

set title "Game Pace given Team Season Avg"
plot 'avg_2d_pace.data' u 2:1:3 w p pt 5 ps 3 palette

