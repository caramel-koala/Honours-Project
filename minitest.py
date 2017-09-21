#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 14 10:58:58 2017

@author: antonio

Runs a small test using tessellations for checking gridding
"""

import tesselvisual as tv
from tessellate import tessellate

planesize = (-2000,2000, -2000, 2000)

sd = 3000

sources = []
n = 5
for i in range(1000,1000+n*10,10):
    sources.append((i,i,5))

cells = tessellate(sources,planesize, 25, 2)

tv.tesselvisual(cells,sources, planesize)