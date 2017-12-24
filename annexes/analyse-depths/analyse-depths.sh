#!/bin/bash

if test -z "$1" || test -z "$2"
then
    echo "Usage $0 min max [precision=1000] < input.dat"
    exit -1
fi

precision=1000
if test -n "$3"
then
    precision="$3"
fi

awk '{rescaled=($3 + 1)/2; if(rescaled < '$2' && rescaled > '$1') print int(rescaled * '$precision')/'$precision'}' | sort -n | uniq -c | ascii-histogram.sh
