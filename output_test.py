# -*- coding: utf-8 -*-
"""
Created on Wed Apr 27 14:30:58 2016

@author: caramelkoala
"""

import numpy as np
import voronoi as vor
import source_gen as sg
#import tesselvisual as tv
from shape import Point
#generate list of galaxies
stellars = []
for i in range(50):
    stellars.append(Point(np.random.random()*6,np.random.random()*6,10000*(np.random.normal(0,0.1)**2)))

#objects above the threshold seleected
source = sg.source_gen(stellars,300)

#generate the initial grid space
plane = [[0,0],[0,6],[6,6],[6,0]]
tangent = [[],0]

#genetate the voronoi cells
cells = vor.Voronoi(source, (0,len(source)-1),tangent)
        
#plot results
#tv.tesselvisual(cells,source)