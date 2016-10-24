
set terminal pngcairo size 600,500 noenhanced font ",18"
set output 'gamePaceWinner.png'

set border linewidth 3 back
#set size square
unset key

set label 1 "hastydata.wordpress.com" at 95,35 font ",12" tc rgb "blue"

set title "Who Controls Pace?"

set xlabel "Team Season Pace"
set xtics 5
set ylabel "Frequency"
set ytics 0.2
set yrange [0.4:0.8]

plot 'getWinner.data' u 1:2 w boxes fs transparent solid 0.25 border lw 2

unset multiplot
