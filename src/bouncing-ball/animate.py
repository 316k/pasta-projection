#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import print_function, division

from sys import argv
import pygame, math
from pygame.locals import *
from time import time
from math import pi
from copy import deepcopy

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


class Sphere:

    def __init__(self, acc_factor=1):
        # self.pos = (maxv - minv) / 2
        # self.pos = np.zeros(3)
        self.pos = np.array([ -4.49713893, -7.06199741, 13.93115129])
        self.velocity = np.random.random(3) - 0.5
        self.velocity /= np.linalg.norm(self.velocity)
        self.velocity *= 150
        # self.acc = np.zeros(3)
        # self.acc_factor = acc_factor

        self.r = 0.5

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

    def intersects(self, pos):
        normalized = pos - self.pos
        return (normalized**2).sum() < self.r**2

def animate(obj1, obj2, path, n):

    # start_time = time()

    stahp = False

    i = 0

    while i < n:
        # dt = time() - start_time
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

        obj1.update(dt)
        obj2.update(dt)
        print(obj1.pos, obj2.pos)
        # Render
        for y in range(h):
            for x in range(w):
                if obj1.intersects(lut3d[y][x]):
                    screen.set_at((x,y), RED)
                if obj2.intersects(lut3d[y][x]):
                    screen.set_at((x,y), GREEN)

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

animate(Sphere(), Sphere(), argv[2] + "/%06d.png", n)
