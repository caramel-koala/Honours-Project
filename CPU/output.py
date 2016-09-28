# -*- coding: utf-8 -*-
"""
Created on Wed Sep 21 10:06:38 2016

@author: caramelkoala
"""

import numpy as np
from source_gen import source_gen
from shape import NewLine, recenter
from voronoi import Voronoi
import gen_cells as gc
import tesselvisual as tv
from stc import source_to_cell

#define the size of the plane for generality
planesize = [600,600]

#generate list of galaxies
sources = []
for i in range(300):
    sources.append((np.random.random()*planesize[0],np.random.random()*planesize[1],abs(np.random.normal(0,0.1))*10000))

#objects above the threshold seleected
stellars = source_gen(sources,700)

#space defined
space = (NewLine((0,0,0),(planesize[0],0,0)),NewLine((0,0,0),(0,planesize[1],0)),NewLine((planesize[0],0,0),(planesize[0],planesize[1],0)),NewLine((0,planesize[1],0),(planesize[0],planesize[1],0)))

#voronoi found
Voronoi(stellars,(0,len(stellars)-1))

source_to_cell(stellars,sources,planesize)

for s in stellars:
	recenter(s)

cells = gc.gen_cells(stellars,planesize,space)

#plot results
tv.tesselvisual(cells,sources)