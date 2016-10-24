
set terminal pngcairo size 600,800 noenhanced
set output 'wheelConditionalLetters.png'

set border linewidth 3 back
#set size square
set key top right
set title "Conditional Frequency of Letters in Final Wheel Puzzle"

set multiplot layout 2,1

set ylabel "Frequency %"
set label 1 "hastydata.wordpress.com" at 13.5,6 font ",12" tc rgb "blue"
set xtics rotate by 0 #font ',14'
set xrange[0:25]
set yrange[0:13]
set ytics 4
set tic scale 0

plot 'finals.hist' using 2:xticlabels(1) w boxes fs transparent solid 0.10 border lw 4 title "Final Wheel", 'finals.hist' using 0:4 w boxes fs transparent solid 0.10 border lw 2 title "R", 'finals.hist' using 0:5 w boxes fs transparent solid 0.10 border lw 2 title "S", 'finals.hist' using 0:6 w boxes fs transparent solid 0.10 border lw 2 title "T", 'finals.hist' using 0:7 w boxes fs transparent solid 0.10 border lw 2 title "L", 'finals.hist' using 0:8 w boxes fs transparent solid 0.10 border lw 2 title "N", 'finals.hist' using 0:9 w boxes fs transparent solid 0.10 border lw 2 title "E"


set title "Conditional Frequency of Letters not in Final Wheel Puzzle"
plot 'finalsNeg.hist' using 2:xticlabels(1) w boxes fs transparent solid 0.10 border lw 4 title "Final Wheel", 'finalsNeg.hist' using 0:4 w boxes fs transparent solid 0.10 border lw 2 title "No R", 'finalsNeg.hist' using 0:5 w boxes fs transparent solid 0.10 border lw 2 title "No S", 'finalsNeg.hist' using 0:6 w boxes fs transparent solid 0.10 border lw 2 title "No T", 'finalsNeg.hist' using 0:7 w boxes fs transparent solid 0.10 border lw 2 title "No L", 'finalsNeg.hist' using 0:8 w boxes fs transparent solid 0.10 border lw 2 title "No N", 'finalsNeg.hist' using 0:9 w boxes fs transparent solid 0.10 border lw 2 title "No E"


