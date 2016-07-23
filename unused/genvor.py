# -*- coding: utf-8 -*-
"""
Created on Mon Jun 27 15:15:19 2016

@author: Caramel Koala
"""
import ldistance as ld
import numpy as np
###############################################################################
def genvor(source,plane):
    if len(source) == 1:
        return [source.append(plane)]
    elif len(source) == 0:
        return [[[0,0],plane]]
    else:
        cells = []
        for s in source:
            cells.append(gen_cell(s,source,plane))
        return cells
############################################################################### 
def gen_cell(x,source,plane):
    #generate list relations between x and other points
    midx = []
    #nearest neighbour placeholder
    nn = [9999]
    for s in source:
        #disregard x from list
        if s[0]==x[0] and s[1]==x[1]:
            continue
        #get perpendicular bisector
        m = -1/(x[1]-s[1])/(x[0]-s[0])
        d = get_midline(x,s,m,plane)
        #find nearest neighbour
        if ld.l2_dist(x,s) < nn[0]:
            nn = [ld.l2_dist(x,s),d]
       
        midx.append(d)

    return [x].append(gen_cycle(nn[1],midx,plane))   
############################################################################### 
def get_midline(o,s,m,plane):
    
    #get midpoint
    x = (o[0] + s[0])/2
    y = (o[1] + s[1])/2
    
    #get intercepts with the plane boundaries
    xd = [plane[0][0],plane[2][0]]
    yd = [plane[0][1],plane[2][1]]

    #get c value
    c = y - m*x 
    
    #find boundary intercepts
    inter = [[xd[0],m*xd[0]+c],[xd[1],m*xd[1]+c],[(yd[0]-c)/m,yd[0]],[(yd[1]-c)/m,yd[1]]]
    
    #remove duplicates
    import itertools
    inter.sort()
    inter = list(inter for inter,_ in itertools.groupby(inter))
    
    #check within boundaires if too many points
    inter = [i for i in inter if i[0]>=xd[0] and i[0]<=xd[1] and i[1]>=yd[0] and i[1]<=yd[1]]
    
    return [[x,y],inter]
###############################################################################
def gen_cycle(n,midx,plane):
    #initiate polygon vertex array
    cycle = []
    
    #set the starting edge to the nearest neigbours edge
    l1 = [n[0],n[1][0]]
    closest = [99999]
    #find the closest intercept to one half of the nearest neighbour edge split by the closest point
    for m in midx:
        l2 = line_intersection(l1,m[1])
        dist = np.sqrt((l1[0][1]-l2[1])**2 + (l1[0][0]-l2[0])**2)
        if dist < closest[0]:
            closest = [dist,l2,m]
    #check if the plane intercepts are closer
    for p in range(len(plane)):
        l2 = line_intersection(l1,[plane[p%4],plane[(p+1)%4]])
        dist = np.sqrt((l1[0][1]-l2[1])**2 + (l1[0][0]-l2[0])**2)
        if dist < closest[0]:
            closest = [dist,l2,m]
        
###############################################################################
def line_intersection(line1, line2):
    xdiff = [line1[0][0] - line1[1][0], line2[0][0] - line2[1][0]]
    ydiff = [line1[0][1] - line1[1][1], line2[0][1] - line2[1][1]]

    def det(a, b):
        return a[0] * b[1] - a[1] * b[0]

    div = det(xdiff, ydiff)
    if div == 0:
       return[9999,9999]

    d = [det(*line1), det(*line2)]
    x = det(d, xdiff) / div
    y = det(d, ydiff) / div
    return [x, y]
###############################################################################