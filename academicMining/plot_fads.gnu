
set terminal pngcairo size 600,1200 noenhanced font ",14"
set output 'fads.png'

set border linewidth 3 back
#set size square

set key top left samplen 1 width 1

#set label 1 "hastydata.wordpress.com" at 0.5,0.9 font ",8" tc rgb "blue"

set xrange[1930:2014]
set xtics 20
set yrange[10:20000]
#set ytics 0.25
set log y

set multiplot layout 3,1
set xlabel "Year"
set ylabel "Pubmed Article Titles"

cd 'data'
set title "Current Scientific trends"
plot './antioxidant.data' w l lw 5 title "Antioxidant", 'autism.data' w l lw 5 title "Autism", 'microbiome.data' w l lw 5 title "Microbiome", './vitamin.data' w l lw 5 title "Vitamin"

set title "Scientific trends of the Recent Past"
plot './cloning.data' w l lw 5 title "Cloning", './gene delivery.data' w l lw 5 title "Gene Delivery", './asperger syndrome.data' w l lw 5 title "Asperger Syndrome", './nanotechnology.data' w l lw 5 title "Nanotechnology"

set title "Ye Olde Scientific trends"
plot './lobotomy.data' w l lw 5 title "Lobotomy", './spleen.data' w l lw 5 title "Spleen", 'gout.data' w l lw 5 title "Gout", 'polio.data' w l lw 5 title "Polio"


unset multiplot
