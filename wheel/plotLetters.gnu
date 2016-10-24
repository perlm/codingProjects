
set terminal pngcairo size 600,400 noenhanced
set output 'wheelLetters.png'

set border linewidth 3 back
#set size square
set key top right
set ylabel "Frequency %"
set title "Frequency of Letters in Final Wheel Puzzle"

set label 1 "hastydata.wordpress.com" at 12.5,10 font ",12" tc rgb "blue"

set xtics rotate by 0 #font ',14'
set xrange[0:25]
set yrange[0:13]
set ytics 4

plot 'finals.hist' using 2:xticlabels(1) w boxes fs transparent solid 0.25 border lw 2 title "Final Wheel", 'finals.hist' u 0:3 w boxes fs transparent solid 0.25 border lw 2 title "English"
