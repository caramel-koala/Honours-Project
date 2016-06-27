# -*- coding: utf-8 -*-
"""
Created on Mon Jun 27 15:15:19 2016

@author: Caramel Koala
"""
import ldistance as ld

def genvor(source, space):
    cells = []
    for s in source:
        cells.append(gen_cell(s,source,space))
        
        
def gen_cell(x,source, space):
    #generate list relations between x and other points
    midx = []
    #nearest neighbour placeholder
    nn = [9999]
    for s in source:
        #disregard x from list
        if s[0]==x[0] and s[1]==x[1]:
            continue
        #relation = [distance,[m,c],[s.x,s.y]]
        d = [ld.l2_dist(s,x),get_mc(x,s),s]
        #find nearest neighbour
        if d[0] < nn[0]:
            nn = d
        midx.append(d)

            
        
        
def get_mc(x,s):
    #m = (y_2- y_1)/(x_2-x_1)
    m = (x[1]-s[1])/(x[0]-s[0])
    #y=mx+c <=> c=y-mx
    c = x[1]-m*x[0]
    
    return [m,c]