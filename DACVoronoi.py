# -*- coding: utf-8 -*-
"""
Created on Sat Aug 06 20:36:34 2016

@author: Caramel Koala
"""
###############################################################################
import Diagram

#generate voronoi diagram
def DACVoronoi(points,space):
    #if only 1 points
    if len(points) == 1:
        #return voronoi cell with entire space as the domain
        return  [[points[0],space]]
    else:
        mid     = int(len(points)/2)
        
        #fork voronoi into left and right branches
        left    = DACVoronoi(points[0:mid],space)
        right   = DACVoronoi(points[mid:len(points)],space)
        
        #return merged voronoi
        return  Diagram.merge(left,right)
###############################################################################