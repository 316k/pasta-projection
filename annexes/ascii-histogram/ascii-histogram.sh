#!/bin/bash

# Save to temp file (for multiple passes)
file=$(mktemp)
cat > $file

function total ()
{
    awk 'BEGIN { total=0 } { total += $1 } END { print total }'
}

function max {
    awk 'BEGIN { max=-18446744073709551616 } { if($1 > max) max = $1 } END { print max }'
}

function maxwidth ()
{
    awk '
BEGIN { max=0 }
{
    len=0;
    for(i=2; i<=NF; i++)
        len += length($i);
    len += i - 2
    if(len > max)
        max = len;
}
END { print max }'
}

max=$(max < $file)
total=$(total < $file)
w=$(maxwidth < $file)

awk '
function rescale(n) {
   return n/'$max' * 100;
}

function percent(n) {
   return n/'$total' * 100;
}

{
    printf("%4d% ", percent($1));

    len = 0;
    for(i=2; i<=NF; i++) {
        printf(" %s", $i);
        len += length($i) + 1;
    }

    # Padding
    for(i=len; i<='$w'; i++)
        printf(" ");

    for(i=0; i < int(rescale($1) * 0.5); i++)
        printf("#");
    if(i == 0)
        printf(".");
    printf(" ");
    print ""
}' $file

rm $file
