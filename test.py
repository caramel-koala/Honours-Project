#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 21 15:39:24 2016

@author: caramelkoala

Test the functionality of the Voronoi creator
"""

import tesselvisual as tv
import numpy as np
from tessellate import tessellate
from math import log

planesize = (-2000,2000, -2000, 2000)

sd = 3000

sources = []
#n = 3
#for i in range(1000,1000+n):
#    for j in range(1000,1000+n):
#        sources.append((i,j,5))

for j in range(1000):
    x = (np.random.randint(planesize[0],planesize[1]) ,np.random.randint(planesize[2],planesize[3]), np.abs(log(np.abs(np.random.normal(0,sd)))))
    if (x[0],x[1],1000) not in sources:
        sources.append(x)
    

#error threshold
e = log(sd)*np.sqrt(planesize[1]*planesize[3])*100

cells = tessellate(sources,planesize, 25, 2)

tv.tesselvisual(cells,sources, planesize)
