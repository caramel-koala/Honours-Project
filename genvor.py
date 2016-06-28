# -*- coding: utf-8 -*-
"""
Created on Mon Jun 27 15:15:19 2016

@author: Caramel Koala
"""
import ldistance as ld
###############################################################################
def genvor(source,plane):
    cells = []
    for s in source:
        cells.append(gen_cell(s,source,plane))
###############################################################################       

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
        d = [m,get_midline(x,s,m,plane)]
        #find nearest neighbour
        if ld.l2_dist(x,s) < nn[0]:
            nn = [ld.l2_dist(x,s),d]
       
        midx.append(d)

    return [x].append(gen_cycle(nn[1],midx,plane))   
    
###############################################################################             
        
###############################################################################         
def get_mc(x,s):
    #m = (y_2- y_1)/(x_2-x_1)
    m = (x[1]-s[1])/(x[0]-s[0])
    #y=mx+c <=> c=y-mx
    c = x[1]-m*x[0]
    
    return [m,c]
############################################################################### 
    
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
    
    return inter
###############################################################################
    
###############################################################################
def gen_cycle(nn,midx,plane):
    cycle = []
    
    
###############################################################################