# -*- coding: utf-8 -*-
"""
Created on Wed Sep 21 10:06:38 2016

@author: caramelkoala
"""

import numpy as np
from shape import NewLine, recenter, source_to_cell, source_gen
from voronoi import Voronoi
import gen_cells as gc
import tesselvisual as tv
from cell_merge import cell_merge
import time

#define the size of the plane for generality
planesize = [600,600]

#generate list of galaxies
sd = 3000 #standard deviation
sources = []
for i in range(20):
    sources.append((np.random.random()*planesize[0],np.random.random()*planesize[1],np.abs(np.random.normal(0,sd))))

#objects above the threshold seleected
stellars = source_gen(sources,0)

#space defined
space = (NewLine((0,0,0),(planesize[0],0,0)),NewLine((0,0,0),(0,planesize[1],0)),NewLine((planesize[0],0,0),(planesize[0],planesize[1],0)),NewLine((0,planesize[1],0),(planesize[0],planesize[1],0)))

#voronoi found
Voronoi(stellars,(0,len(stellars)-1))

#append sources to cell, recentre and compute error
source_to_cell(stellars,sources,planesize)
recenter(stellars)

cells = gc.gen_cells(stellars,planesize,space)

#plot results
tv.tesselvisual(cells,sources)

#error threshold

e = sd*np.sqrt(planesize[0]*planesize[1])*len(sources)

start = time.time()
cell_merge(stellars,e)
end = time.time()

print end - start
  
cells = gc.gen_cells(stellars,planesize,space)

#plot results
tv.tesselvisual(cells,sources)