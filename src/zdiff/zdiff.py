#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import division

from sys import argv
import numpy as np

from img import *

if len(argv) < 3:
    print("Usage: %s lut1.ppm out.dat [out.pgm]" % argv[0])
    exit()

# Max blue channel value
threshold = 0.5

# first image
img, img_depth = read_img(argv[1])

out = -np.ones(img.shape, dtype=float)

for y, row in enumerate(img):
    for x, col in enumerate(row):
        out[y][x][0] = x
        out[y][x][1] = y

        # col = [x, y, error]
        if col[2]/img_depth < threshold:
            out[y][x][2] = x/img.shape[1] - col[0]/img_depth

np.savetxt(argv[2], out.reshape((out.shape[0] * out.shape[1], out.shape[2])), fmt="%d %d %f")

if len(argv) > 3:
    depths = out[:, :, 2].flatten()
    recalee = (out[:, :, 2] + 1)/2.0 * 65535
    write_img(argv[3], recalee, 16)
