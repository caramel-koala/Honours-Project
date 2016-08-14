# -*- coding: utf-8 -*-
"""
Created on Sat Aug 06 20:36:34 2016

@author: Caramel Koala
"""
from scipy.spatial import ConvexHull
###############################################################################
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
        return  merge(left,right,space)
###############################################################################
#merge algorithm for joining voronois
def merge(left,right,space):
    #get the convex hull of left
    if len(left)>3:
        lhull   = convex_hull(left)
    else:
        lhull   = left
     #get convex hull of right  
    if len(right)>3:
        rhull   = convex_hull(right)
    else:
        rhull   = right
        
    #find lowest common support line    
    LCS = find_LCS(lhull,rhull,space)
    
    return LCS
    
###############################################################################    
#Calculate biisector
def biSector(p1,p2):
    mid = [(p1[0]+p2[0])/2,(p1[1]+p2[1])/2]
    m   = -(p1[0]-p2[0])/float(p1[1]-p2[1])
    return  [mid,m] #return midpoint and gradient of bisector
###############################################################################
#get convex hull of cells
def convex_hull(cells):
    cen     = []
    for cell in cells: cen.append([cell[0][0],cell[0][1]])
    hullt   = list(ConvexHull(cen).simplices)
    hull    = []
    line    = hullt[0]
    hull.append(cells[line[0]])
    del hullt[0]
    while not len(hullt) == 0:
        join    = line[1]
        for i,l in enumerate(hullt):
            if l[0] == join:
                line = l
                del hullt[i]
                break
            if l[1] == join:
                line = [l[1],l[0]]
                del hullt[i]
                break
        hull.append(cells[line[0]])
    return hull
###############################################################################
#find the intercept of two hulls
def hull_intercept(po,pa,pb):
    return (pa[0]-po[0])*(pb[1]-po[1])-(pa[1]-po[1])*(pb[0]-po[0])
###############################################################################
#find the lowest common support line between the convex hulls
#gives our merge a starting point at the bottom
def find_LCS(lpoly,rpoly):
    
    #find the rightmost left point
    u = lpoly[0]
    for cell in lpoly:
        if cell[0][0] > u[0][0]:
            u = cell
    #find the leftmost right point        
    v = rpoly[0]      
    for cell in rpoly:
        if cell[0][0] < v[0][0]:
            v = cell
    #find LCS (lowest bisector of hulls)       
    L   = 
     
    return lpoly+rpoly
    