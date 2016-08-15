# -*- coding: utf-8 -*-
"""
Created on Wed Apr 27 14:30:58 2016

@author: caramelkoala
"""

import numpy as np
import layout as lay
#import source_gen as sg
from operator import attrgetter
import tesselvisual as tv
from shape import *
from gen_cells import *

#define the size of the plane for generality
planesize = [600,600]

#generate list of galaxies
stellars = []
for i in range(500):
    stellars.append(Point(np.random.random()*planesize[0],np.random.random()*planesize[1]))#,10000*(np.random.normal(0,0.1)**2)))

#objects above the threshold seleected
#source = sg.source_gen(stellars,300)

#sort objects by x-axis
stellars.sort(key=attrgetter('x','y'))

#create space for voronoi to fill
space = (Line(Point(0,0),Point(planesize[0],0)),Line(Point(0,0),Point(0,planesize[1])),Line(Point(planesize[0],0),Point(planesize[0],planesize[1])),Line(Point(0,planesize[1]),Point(planesize[0],planesize[1])))

#generate the voronoi
vorspace = lay.VoronoiSpace(stellars,space)
vorspace.Voronoi((0,len(stellars)-1))

cells = gen_cells(vorspace,planesize)

#plot results
tv.tesselvisual(cells,stellars)