
set terminal pngcairo size 1250,500 noenhanced
set output 'refs.png'

set border linewidth 3 back
#set size square
unset key
set title "NBA Refs and Number of Fouls"

set label 1 "hastydata.wordpress.com" at 1,52.5 font ",12" tc rgb "blue"

set xtics rotate by -60 font ',10'
set yrange[30:55]
set ylabel "Number of Fouls per Game" textcolor rgb "red"
set ytics 5 nomirror
set y2label "Number Of Games Officiated" textcolor rgb "blue"
set y2range[0:500]
set y2tics 100

plot 'data/refFoulsAve.data' using ($4>=3?$2:1/0):xticlabels(1) w p lw 2 pt 7 ps 1 lc 1 notitle, 'data/refFoulsAve.data' using 0:($4>=3?$2:1/0):3 w errorbars lw 2 pt 7 ps 1 lc 1 notitle, 'data/refFoulsAve.data' using 0:($4>=3?$4:1/0) axes x1y2 w boxes fs transparent solid 0.1 notitle

