
set terminal pngcairo size 1000,500 noenhanced font ",16"
set output 'expected.png'

set border linewidth 3 back
set size square
set grid lw 3
set key bottom right width 0 samplen 0

set multiplot layout 1,2

#set label 1 "hastydata.wordpress.com" at 0.025,0.875 font ",12" tc rgb "blue"

# -0.00683882035643426 0.0244368322763766 0.0282614304017384
# -0.00654231617038214 0.0235555799395371 0.030369350985866
# -0.018887114322177 0.0231058621375531 0.0364739665650321
set xrange[0.5:1]
set xtics 0.25
set yrange[1.5:3]
set ytics 0.5

set title "Technical Foul FT Stragies"
set ylabel "Expected Points"
set xlabel "Foulee FT%"
plot (0.8-0.018887114322177) + (x-0.018887114322177) + (x+0.0231058621375531) w l lw 3 title "TF FT 80%", (0.75-0.018887114322177) + (x-0.018887114322177) + (x+0.0231058621375531) w l lw 3 lc rgb "dark-green" title "TF FT 75%", (x-0.018887114322177) + (x+0.0231058621375531)+ (x+0.0364739665650321) w l lw 3 lc 3 title "Foulee all three"

set xlabel "TF FT% - Foulee FT%"
set ylabel "Difference in Expected Points"
set xrange[0:0.25]
set xtics 0.05
set yrange[-0.5:0.5]
set ytics 0.25
plot x-0.018887114322177-0.0364739665650321  w l lw 3  notitle

unset multiplot

