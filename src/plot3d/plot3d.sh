#!/usr/bin/bash

nx=$(awk '{print $1}' $1 | sort | uniq | wc -l)
ny=$(awk '{print $2}' $1 | sort | uniq | wc -l)
echo $nx $ny

gnuplot <<EOF
set terminal png size 1920,1080 enhanced
set output 'gnuplotout.png'
set ticslevel 0
set dgrid3d ${nx}/2,${ny}/2
set hidden3d
splot "${1}" u 1:2:3 with lines
pause mouse button2
EOF

