# -*- coding: utf-8 -*-
"""
Created on Wed Apr 27 14:30:58 2016

@author: caramelkoala
"""

import numpy as np
import layout as lay
from operator import attrgetter
#import source_gen as sg
#import tesselvisual as tv
from shape import Point


#generate list of galaxies
stellars = []
for i in range(50):
    stellars.append(Point(int(np.random.random()*610),int(np.random.random()*610)))#,10000*(np.random.normal(0,0.1)**2)))

#objects above the threshold seleected
#source = sg.source_gen(stellars,300)

#sort objects by x-axis
stellars.sort(key=attrgetter('x','y'))

#generate the voronoi space
vor = lay.VoronoiSpace(stellars)

#genetate the voronoi cells
cells = vor.Voronoi((0,len(stellars)-1))


        
#plot results
#tv.tesselvisual(cells,source)