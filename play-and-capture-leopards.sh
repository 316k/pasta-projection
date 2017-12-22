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

# totem doit être lancé en full screen (sur pause) dans le projecteur (leos-framerate2.mp4)
# la caméra doit être disponible

mkdir "$1"

totem --pause; totem --seek-bwd
sleep 1

(sleep 2.5; totem --play) &

timeout 180 ./capture.sh "$1" $2

