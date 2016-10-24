
set terminal pngcairo size 1000,500 noenhanced font ",14"
set output 'techs.png'

set border linewidth 3 back
set size square


set label 1 "hastydata.wordpress.com" at 1.1,0.012 font ",14" tc rgb "blue"

set style fill solid 0.25 border lt -1
set style boxplot 
set style data boxplot

set ylabel "Technicals per Minute"
set xlabel "Player Country of Birth"

set xtics ('US' 1, 'International' 2)
plot for [i=1:2] 'summary.data' using (i):i notitle

