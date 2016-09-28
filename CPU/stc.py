# -*- coding: utf-8 -*-
"""
Created on Wed Sep 28 11:19:09 2016

@author: caramelkoala
"""
from shape import distance

def source_to_cell(points, sources, size):
    
    for source in sources:
        min_dist = size[0]*size[1] #starting minimum is the greatest possible distance
        minpoint = None
        
        for p in points:
            d = distance(source,p)
            if d < min_dist:
                min_dist = d
                minpoint = p
        
        minpoint[7].append(source)