
set terminal pngcairo size 500,500 noenhanced font ",14"
set output 'histogram.png'
#set terminal svg size 500,500 noenhanced font ",14"
#set output 'histogram.svg'

set border linewidth 3 back
set size square

set label 1 "hastydata.wordpress.com" at 2,0.375 font ",8" tc rgb "blue"

set style fill solid 0.25 border lt -1
set style boxplot 
set style data boxplot

set ylabel "FT%"
set xtics ("All" 0,"First" 1, "Second" 2, "Third" 3)
#plot 'data/freeThrows.data.backup' using (0):(($2+$4+$6)/($3+$5+$7)) notitle,  'data/freeThrows.data.backup' using (1):(($2)/($3)) notitle, 'data/freeThrows.data.backup' using (2):(($4)/($5)) notitle, 'data/freeThrows.data.backup' using (3):(($6)/($7)) notitle,
plot 'data/freeThrows.data' using (0):($3>50?($2+$4+$6)/($3+$5+$7):1/0) lc rgb "red" notitle,  'data/freeThrows.data' using (1):($3>50?($2)/($3):1/0) lc rgb "dark-green" notitle, 'data/freeThrows.data' using (2):($5>50?($4)/($5):1/0) lc rgb "blue" notitle, 'data/freeThrows.data' using (3):($7>10?($6)/($7):1/0) notitle #, 'average.data' u 1:2 w p pt 7 ps 2 lc rgb "red" notitle

