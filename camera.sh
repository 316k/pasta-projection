#!/bin/bash
exp=150000

if [ -n "$1" ]
then
    exp="$1"
fi

playCamera -pasta -exposure $exp
