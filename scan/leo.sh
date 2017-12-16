#!/bin/bash

function fiximages {

    i=$1
    cd $i

    ../../src/remove-duplicates/remove-duplicates.py . cam*.png

    cd ..
}



mkdir match

flip=../../../src/flip-lut/flip-lut-single

i=$1


#for i in $(seq 1 11)
#do
    if ! test -e $i/000.png
    then
        fiximages $i
    fi

    cd match

    mkdir $i
    cd $i
    dir=$(ls -d ../../$i/ 2>/dev/null || ls -d ../../$i/ 2>/dev/null)
    playLeopard -cam $dir%03d.png -proj ../../../leo/leopard_1280_720_32B_%03d.png -number 101 -display

    convert lutProj15.png lut.ppm
    convert maxCam.png cam.pgm

    $flip cam.pgm lut.ppm > $i.orig.pgm
    convert $i.orig.pgm -median 5 ../checkerboard$i.png

    cd ..

    cd ..
#done
