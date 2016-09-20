# -*- coding: utf-8 -*-
"""
Created on Wed Apr 27 14:30:58 2016

@author: caramelkoala
"""

import numpy as np
import layout as lay
import source_gen as sg
import tesselvisual as tv
from shape import Source, Line, Point
import gen_cells as gc

#define the size of the plane for generality
planesize = [600,600]

#generate list of galaxies
sources = []
for i in range(300):
    sources.append(Source(np.random.random()*planesize[0],np.random.random()*planesize[1],np.log10(abs(np.random.normal(0,0.1))*10000)))

#objects above the threshold seleected
stellars = sg.source_gen(sources,3)

#create space for voronoi to fill
space = (Line(Point(0,0,0),Point(planesize[0],0,0)),Line(Point(0,0,0),Point(0,planesize[1],0)),Line(Point(planesize[0],0,0),Point(planesize[0],planesize[1],0)),Line(Point(0,planesize[1],0),Point(planesize[0],planesize[1],0)))

#generate the voronoi
vorspace = lay.VoronoiSpace(stellars,space)
vorspace.Voronoi((0,len(stellars)-1))

cells = gc.gen_cells(vorspace,planesize)

#plot results
tv.tesselvisual(cells,sources)