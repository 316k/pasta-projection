#!/bin/bash
if [ -z "$1" ]
then
    echo usage: $0 dest-folder [exposition=150000]
    exit
fi

exp=150000

if [ -n "$2" ]
then
    exp="$2"
fi


cd $1
playCamera -pasta -exposure $exp -fps 1 -save cam%03d.png
