#!/usr/bin/python
# -*- coding: utf-8 -*-

from PIL import Image
from sys import argv
import numpy as np

def img(path):
    im = Image.open(path)
    return np.array(im.getdata()), im

if len(argv) < 3:
    print("Usage: %s dir file1 file2 [...]" % argv[0])
    exit()

thresh = 2

outdir = argv[1]

# first image
last, im = img(argv[2])
im.save(outdir + '/000.png')

i = 1

for num, f in enumerate(argv[3:]):
    new, im = img(f)

    diff = abs(new - last).sum() / new.size

    print(num + 1, diff)
    if diff > thresh:
        
        im.save(outdir + "/%03d.png" % i)
        i += 1

    last = new
