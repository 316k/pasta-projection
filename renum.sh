#!/bin/bash
count=0
for i in *
do
    ext=$(echo $i | sed -r 's/.+\.([^.]+)$/\1/')
    num=$(printf "%03d" $count)
    mv "$i" "$num.$ext"
    let count++
done
