#!/bin/bash
exp=150000

if [ -z "$1" ]
then
    echo usage: $0 dest.avi "[exposition=$exp]"
    exit
fi

if [ -n "$2" ]
then
    exp="$2"
fi

playCamera -pasta -exposure $exp -savevideo "$1"
