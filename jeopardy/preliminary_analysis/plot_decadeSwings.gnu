
set terminal pngcairo size 500,1000 noenhanced
set output 'decadeSwing.png'

set multiplot layout 2,1
set border linewidth 3 back

#set size square
unset key

set ylabel "Number of Appearances (2010s-1990s)"
set yrange[-35:35]
set xrange[0:15]
set xtics rotate by -60 font ',13'
set label 1 "hastydata.wordpress.com" at 6,-25 font ",13" tc rgb "blue"

set title "More Frequent Jeopardy Clues
plot 'decadeSwing1990s.data' using 2:xticlabels(1) w boxes fs solid 0.25 border lw 3

set label 1 "hastydata.wordpress.com" at 5,25 font ",13" tc rgb "blue"
set title "Less Frequent Jeopardy Clues
plot 'decadeSwing1990sLess.data' using 2:xticlabels(1) w boxes fs solid 0.25 border lw 3 

unset multiplot
