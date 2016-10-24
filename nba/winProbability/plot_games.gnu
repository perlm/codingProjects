
set terminal pngcairo size 600,800 noenhanced font ",18"
set output 'games.png'
#need to use old version of gnuplot until i figure it out...
# /usr/bin/gnuplot

#set terminal svg size 600,800 font "Arial,18"
#set output 'games.svg'

set border linewidth 3 back
#set size square
unset key

#set label 1 "hastydata.wordpress.com" at 0.6,0.6 font ",8" tc rgb "blue"

set xrange[0:48]
set xtics 6

set yrange[-5:35]
set ytics 10 nomirror

set y2range[0:1]
set y2tics 0.25

set multiplot layout 2,1
set xlabel "Minutes Elapsed"
set ylabel "Score Differential\n(Home-Away)" textcolor rgb "blue"
set y2label "Home Team Win Probability" textcolor rgb "red"

set title "Random Game"
plot 'data/game_0.data' u 1:2 w lp pt 5 lc 3 lw 3, 'data/game_0.data' u 1:3 axes x1y2 w lp pt 7 lc 1 lw 3 ps 1

set title "Most Unlikely Game"
plot 'data/game_152400.data' u 1:2 w lp pt 5 lc 3 lw 3, 'data/game_152400.data' u 1:3 axes x1y2 w lp pt 7 lc 1 lw 3 ps 1
unset multiplot

