#!/bin/bash
exp=150000

if [ -z "$1" ]
then
    echo usage: $0 dest-folder/ "[exposition=$exp]"
    exit
fi

if [ -n "$2" ]
then
    exp="$2"
fi

cd $1
playCamera -pasta -exposure $exp -fps 16 -save cam%03d.png
