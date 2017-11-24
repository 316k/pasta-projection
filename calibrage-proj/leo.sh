#!/bin/bash
cd match
for i in $(seq 1 10)
do
    mkdir $i
    cd $i
    playLeopard -cam ../../$i/%03d.png -proj ../../../leo/leopard_1280_720_32B_%03d.png -number 101 -display -iter 25
    cd ..
done
