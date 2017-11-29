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

# totem doit être lancé en full screen (sur pause) dans le projecteur
# la caméra doit être disponible

mkdir "$1"

totem leos.mp4; totem --pause; totem --seek-bwd
sleep 1

(sleep 2.3; totem --play) &

timeout 110 ./capture.sh $1 $2
