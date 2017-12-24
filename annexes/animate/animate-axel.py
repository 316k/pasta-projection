#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import print_function, division

from os.path import isfile
from sys import argv
import pygame, math
from pygame.locals import *
from time import time
from math import pi
from copy import deepcopy

import pickle
import hashlib

def md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


import numpy as np
from img import *

WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0, 255, 0)
BLUE = (0,0,255)


w, h = 1280, 720

start_time = time()

clock = pygame.time.Clock()

bkg = BLACK

class Obj3D:

    def __init__(self, acc_factor=1):
        self.pos = (maxv - minv) / 2
        # self.pos = np.zeros(3)
        # self.pos = np.array([ -4.49713893, -7.06199741, 13.93115129])
        self.velocity = np.random.random(3) - 0.5
        self.velocity /= np.linalg.norm(self.velocity)
        self.velocity *= 150
        # self.acc = np.zeros(3)
        # self.acc_factor = acc_factor


    def update(self, dt):
        # self.velocity += dt * self.acc_factor * self.acc
        self.pos += dt * self.velocity

        if any(self.pos < minv) or any(self.pos > maxv):
            for coor in range(3):
                if self.pos[coor] < minv[coor] or self.pos[coor] > maxv[coor]:
                    self.pos[coor] -= dt * self.velocity[coor] # back in time
            self.velocity = np.random.random(3) - 0.5
            self.velocity /= np.linalg.norm(self.velocity)
            self.velocity *= 150

class Sphere(Obj3D):

    def __init__(self, acc_factor=1):
        
        Obj3D.__init__(self, acc_factor)
        self.r = 1

    def intersects(self, pos):
        normalized = pos - self.pos
        return (normalized**2).sum() < self.r**2

    def bounding_box(self):
        return map(lambda x: int(x - self.r), self.pos), map(lambda x: int(x + self.r), self.pos)

class Plane(Obj3D):
    def __init__(self, acc_factor=1):
        
        Obj3D.__init__(self, acc_factor)

        self.velocity[0] = 0
        self.velocity[1] = 0
        self.velocity[2] = 150

    def intersects(self, pos):
        normalized = pos - self.pos
        return -0.5 < normalized[2] < 0.5

    def bounding_box(self):
        return (int(minv[0]), minv[1], int(self.pos[2] - 0.5)), (int(maxv[0]), int(maxv[1]), int(self.pos[2] + 0.5))

def animate(objects, path, n):

    # start_time = time()

    stahp = False

    i = 0

    while i < n:
        # dt = (time() - start_time) * 1000
        dt = 0.0040
        screen.fill(bkg)

        for e in pygame.event.get():
            if e.type is QUIT:
                stahp = True
            elif e.type is KEYDOWN:
                if e.key == K_ESCAPE:
                    stahp = True
                # elif e.key == K_a:
                #     obj.acc[2] = -1
                # elif e.key == K_d:
                #     obj.acc[2] = 1
                # elif e.key == K_w:
                #     obj.acc[1] = -1
                # elif e.key == K_s:
                #     obj.acc[1] = 1
                # elif e.key == K_q:
                #     obj.acc[0] = -1
                # elif e.key == K_e:
                #     obj.acc[0] = 1

        for obj, color in objects:

            obj.update(dt)

            bbmin, bbmax = obj.bounding_box()

            for x in range(bbmin[0], bbmax[0] + 1):
                for y in range(bbmin[1], bbmax[1] + 1):
                    for z in range(bbmin[2], bbmax[2] + 1):

                        coords = np.array((x, y, z)) - minv

                        if all(0 <= coords) and all(coords < maxv - minv):
                            pixels = grid[coords[0]][coords[1]][coords[2]]

                            for p in pixels:
                                ximg, yimg = p

                                if obj.intersects(lut3d[yimg][ximg]):
                                    screen.set_at(p, color)


        # pygame.display.flip()
        # clock.tick(30)
        # start_time = time()

        pygame.image.save(screen, path % i)
        i += 1


if len(argv) < 3:
    print("usage: %s lut3d.ppm dir/ [n=3000]" % argv[0])
    exit()

lut3d, _ = read_img(argv[1])

minv = np.array([-7, -8, 0])
maxv = np.array([20, 8, 22])

lut3d = (lut3d / 65535) * (maxv - minv) + minv

screen = pygame.display.set_mode((w, h), 0 & FULLSCREEN)
pygame.display.set_caption("Animation")

n = 3000
if len(argv) >= 4:
    n = int(argv[3])

lut_hash = md5(argv[1])

pickle_fname = lut_hash + '.pickle'

if isfile(pickle_fname):
    print("Loading pickled grid from ", pickle_fname)
    grid = pickle.load(open(pickle_fname, 'rb'))
else:
    print("Pre-building grid")
    # Build grid
    grid_size = 1

    grid = [[[[] for k in range(int((maxv - minv)[2] / grid_size))] for i in range(int((maxv - minv)[1] / grid_size))] for j in range(int((maxv - minv)[0] / grid_size))]

    for y in range(h):
        for x in range(w):
            world = map(int, lut3d[y][x])
            xw, yw, zw = world - minv
            if xw + yw + zw != 0:
                grid[int(xw)][int(yw)][int(zw)].append((x, y))

    print("Grid built, pickling data")
    pickle.dump(grid, open(pickle_fname, 'wb'))

# animate([(Sphere(), RED), (Sphere(), BLUE), (Sphere(), GREEN), (Sphere(), WHITE)], argv[2] + "/%06d.png", n)
animate([(Plane(), GREEN)], argv[2] + "/%06d.png", n)
