#!/bin/bash
if [ -z "$1" ]
then
    echo usage: $0 dest-folder
    exit
fi

cd $1
playCamera -pasta -exposure 150000 -fps 1 -save checkerboard%03d.png
