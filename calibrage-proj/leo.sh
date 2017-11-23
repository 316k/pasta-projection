#!/bin/bash
cd match
mkdir $1
cd $1
playLeopard -cam ../../$1/%03d.png -proj ../../../leo/leopard_1280_720_32B_%03d.png -number 101 -display
