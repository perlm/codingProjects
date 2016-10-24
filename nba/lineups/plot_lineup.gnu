
set terminal pngcairo size 500,500 noenhanced
set output 'lineup.png'

#set size square
unset key
set ylabel "Relative Performance"
set title "Performance of 'Height Parity' Lineups"
set yrange[0.85:1.15]

set label 1 "hastydata.wordpress.com" at 3.25,1.125 font ",10" tc rgb "blue"

set xtics rotate by -60 font ',12'

set boxwidth 0.75

plot 'ave.data' using ($2/$4):xticlabels(1) w boxes fs transparent solid 0.5 border notitle, 'ave.data' using ($0):($2/$4):($3/$4) w errorbars lw 2 lc 1

#plot 'ave.data' using ($2/$4):xticlabels(1):($3/$4):($3/$4) w boxerrorbars fs transparent solid 0.5 border
