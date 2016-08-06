# -*- coding: utf-8 -*-
"""
Created on Sat Aug 06 20:36:34 2016

@author: Caramel Koala
"""
###############################################################################
import Diagram

#generate voronoi diagram
def DACVoronoi(points,space):
    #if only 2 points
    if len(points) ==2:
        lower   = points[0]
        upper   = points[1]
        
        line    = [biSector(lower,upper)]

        #calculate Voronoi of 2 points
        return  Diagram.VD(line,points,space)
    #if only 1 points
    elif len(points) == 1:
        #return voronoi with entire space as the domain
        return  Diagram.VD([],points,space)
    else:
        mid     = int(len(points)/2)
        
        #fork voronoi into left and right branches
        left    = DACVoronoi(points[0:mid],space)
        right   = DACVoronoi(points[mid+1:len(points)],space)
        
        #return merged voronoi
        return  Diagram.merge(left,right)
###############################################################################
#Calculate biisector
def biSector(p1,p2):
    mid = [(p1[0]+p2[0])/2,(p1[1]+p2[1])/2]
    m   = -(p1[0]-p2[0])/float(p1[1]-p2[1])
    return  [mid,m] #return midpoint and gradient of bisector
###############################################################################