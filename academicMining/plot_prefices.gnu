
set terminal pngcairo size 600,600 noenhanced font ",14"
set output 'prefices.png'

set border linewidth 3 back
set size square

set key top left

set label 1 "hastydata.wordpress.com" at 1962,1000 font ",12" tc rgb "blue"

set xrange[1930:2014]
set xtics 20
set yrange[:2000]
#set ytics 0.25
set log y

#set multiplot layout 1,2
set xlabel "Year"
set ylabel "Pubmed Article Titles"

cd 'data'
set title "Metric Prefices and Science Titles"
plot './micro.data' w lp lw 3 title "Micro", './nano.data' w lp lw 3 title "Nano", './pico.data' w lp lw 3 title "Pico", './femto.data' w lp lw 3 title "Femto"


#unset multiplot
