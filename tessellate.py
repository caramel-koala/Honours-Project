# -*- coding: utf-8 -*-
"""
Created on Wed Sep 21 10:06:38 2016

@author: caramelkoala
"""

from shape import recenter, source_to_cell, source_gen
from voronoi import Voronoi
from cell_merge import cell_merge
from gpu_merge import gpu_merge
import time

###############################################################################
def tessellate(sources,threshold,error,host,planesize):
    #objects above the threshold seleected
    stellars = source_gen(sources,threshold)
    
    #voronoi found
    Voronoi(stellars,(0,len(stellars)-1))
    
    #append sources to cell, recentre and compute error
    source_to_cell(stellars,sources,planesize)
    recenter(stellars)
    
    e = 0
    for p in stellars:
        e += p[8]

    if (host == 1):
        #gpu merge
        start = time.time()
        e = gpu_merge(stellars,error,len(sources))
        end = time.time()
        return (stellars,end - start,e)
    elif (host == 0):    
        #cpu merge
        start = time.time()
        e = cell_merge(stellars,error)
        end = time.time()
        return (stellars,end - start,e)
        
    return (stellars,0,e)
###############################################################################