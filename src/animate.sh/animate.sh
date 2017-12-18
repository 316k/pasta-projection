#!/bin/bash

if [ -z "$3" ]
then
    echo "usage: $0 disparity-map.pgm min1 max1 [min2 max2 [min3 max3 ...]]"
    exit -1
fi

disparitymap="$1"
shift 1

dir=$(mktemp -d)

# Produire N outputs
n=0
while [ -n "$1" ]
do
    disparity-to-colors.py "$disparitymap" "$1" "$2" $dir/$n.ppm
    let n++
    shift 2
done

eog $dir/*.ppm

rm -r $dir

echo "
0.481 0.522
0.536 0.545
0.55 0.577
0.583 0.59"
