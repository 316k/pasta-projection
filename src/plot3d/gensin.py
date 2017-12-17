#!/usr/bin/python3

from math import sin, pi

with open('sine.dat', "w") as f:
    for x in range(1000):
        for y in range(1000):
               f.write(' '.join([str(x), str(y), str(sin(2 * pi * x / 50))]) + '\n')
