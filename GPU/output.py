# -*- coding: utf-8 -*-
"""
Created on Wed Sep 21 10:06:38 2016

@author: caramelkoala
"""

import numpy as np
from source_gen import source_gen
from shape import NewLine
from layout import Voronoi

#define the size of the plane for generality
planesize = [600,600]

#generate list of galaxies
sources = []
for i in range(300):
    sources.append((np.random.random()*planesize[0],np.random.random()*planesize[1],np.log10(abs(np.random.normal(0,0.1))*10000)))

#objects above the threshold seleected
stellars = source_gen(sources,3)

#space defined
space = (NewLine((0,0,0),(planesize[0],0,0)),NewLine((0,0,0),(0,planesize[1],0)),NewLine((planesize[0],0,0),(planesize[0],planesize[1],0)),NewLine((0,planesize[1],0),(planesize[0],planesize[1],0)))

#voronoi found
vorspace = Voronoi(stellars,space,(0,len(stellars)-1))

cells = gc.gen_cells(vorspace,planesize)