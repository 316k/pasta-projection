#!/bin/bash

if [ -z "$3" ]
then
    echo "usage: $0 depth-map.pgm min1 max1 [min2 max2 [min3 max3 ...]]"
    exit -1
fi

depthmap="$1"
shift 1

dir=$(mktemp -d)

# Produire N outputs
n=0
while [ -n "$1" ]
do
    echo $1S
    depths-to-colors.py "$depthmap" "$1" "$2" $dir/$n.ppm
    let n++
    shift 2
done

eog $dir/*.ppm
exit

echo "
481 522
536 545
55 577
583 59"
