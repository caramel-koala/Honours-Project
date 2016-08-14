# -*- coding: utf-8 -*-
"""
Created on Wed Apr 27 14:30:58 2016

@author: caramelkoala
"""

import numpy as np
import DACVoronoi as DV
#import source_gen as sg
import tesselvisual as tv


#generate list of galaxies
stellars = []
for i in range(50):
    stellars.append([np.random.random()*610,np.random.random()*610])#,10000*(np.random.normal(0,0.1)**2)))

#objects above the threshold seleected
#source = sg.source_gen(stellars,300)

#sort objects by x-axis
stellars.sort(key=lambda x: (x[0],x[1]))

#create space for voronoi to fill
space = [[0,0],[0,610],[610,610],[610,0]]

#generate the voronoi 
cells = DV.DACVoronoi(stellars,space)

        
#plot results
tv.tesselvisual(cells,stellars)