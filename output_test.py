# -*- coding: utf-8 -*-
"""
Created on Wed Apr 27 14:30:58 2016

@author: caramelkoala
"""

import numpy as np
import tesselvisual as tv

#generate grid of centres
cells = []
for i in range(3):
    for j in range(3):
        x = 2*i+1
        y = 2*j+1
        cells.append([[x,y],[x-1,y-1],[x+1,y-1],[x+1,y+1],[x-1,y+1]])
        
#generate list of galaxies
stellars = []
for i in range(500):
    stellars.append([np.random.normal(3,1),np.random.normal(3,1),10000*(np.random.normal(0,0.1)**2)])
    
#plot results
tv.tesselvisual(cells,stellars)