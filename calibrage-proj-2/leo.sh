#!/bin/bash
mkdir match-higher-expo
cd match-higher-expo
for i in $(seq 1 11)
do
    mkdir $i
    cd $i
    dir=$(ls -d ../../$i-17*/ 2>/dev/null || ls -d ../../$i-19*/ 2>/dev/null)
    playLeopard -cam $dir%03d.png -proj ../../../leo/leopard_1280_720_32B_%03d.png -number 101 -display -iter 25
    cd ..
done
