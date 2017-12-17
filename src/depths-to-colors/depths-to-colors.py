#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import division

from sys import argv
import numpy as np

from colorsys import hsv_to_rgb

from img import *

if len(argv) < 5:
    print "Usage %s file min max out.ppm" % argv[0]
    exit(-1)

img, img_depth = read_img(argv[1])
img /= img_depth

low, high = float(argv[2]), float(argv[3])

out = np.zeros((img.shape[0], img.shape[1], 3))

for y in range(img.shape[0]):
    for x in range(img.shape[1]):
        if low < img[y][x] < high:
            c = hsv_to_rgb((img[y][x] - low) / (high - low), 1, 1)
            out[y][x] = c

write_img(argv[4], out * 65535, 16)
