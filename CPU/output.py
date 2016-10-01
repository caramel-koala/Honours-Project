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

#define the size of the plane for generality
planesize = [600,600]

#generate list of galaxies
sources = []
for i in range(100):
    sources.append((np.random.random()*planesize[0],np.random.random()*planesize[1],np.abs(np.random.normal(0,3000))))

#objects above the threshold seleected
stellars = source_gen(sources,3000)

#space defined
space = (NewLine((0,0,0),(planesize[0],0,0)),NewLine((0,0,0),(0,planesize[1],0)),NewLine((planesize[0],0,0),(planesize[0],planesize[1],0)),NewLine((0,planesize[1],0),(planesize[0],planesize[1],0)))

#voronoi found
Voronoi(stellars,(0,len(stellars)-1))

source_to_cell(stellars,sources,planesize)

cells = gc.gen_cells(stellars,planesize,space)

#plot results
tv.tesselvisual(cells,sources)

recenter(stellars)

cells = gc.gen_cells(stellars,planesize,space)

#plot results
tv.tesselvisual(cells,sources)

for i in xrange(10):
    cell_merge(stellars)
    
    cells = gc.gen_cells(stellars,planesize,space)
    
    #plot results
    tv.tesselvisual(cells,sources)