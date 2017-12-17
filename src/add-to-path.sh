#!/bin/bash

dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

for d in "$dir"/*
do
    if ! test -d "$d"
    then
        continue
    fi

    PATH="$d:$PATH"
done

export PATH
