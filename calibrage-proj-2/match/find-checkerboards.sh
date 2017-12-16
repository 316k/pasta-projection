#!/bin/bash

flip=../../src/flip-lut/flip-lut

for i in $(seq 1 11)
do
    convert $i/lutProj25.png lut.ppm
    convert $i/maxCam.png cam.pgm
    $flip cam.pgm lut.ppm > $i.orig.pgm
    convert $i.orig.pgm -median 5 damiers/checkerboard$i.png
done
