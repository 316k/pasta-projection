#!/bin/bash

if [ -z "$1" ]
then
    echo usage: $0 dest-folder
    exit
fi

# totem doit être lancé en full screen (sur pause) dans le projecteur
# la caméra doit être disponible

(sleep 2.3; totem --play) &
timeout 210 ./capture.sh $1
