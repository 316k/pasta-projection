#!/bin/bash
for i in $(seq 1 10)
do
    cd $i
    convert -separate lutProj15.png lutProj15-channels.png
    cp lutProj15-channels-2.png ../checkerboard-$i.png
    cd ..
done
