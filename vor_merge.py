# -*- coding: utf-8 -*-
"""
Created on Tue Jun 21 19:09:14 2016

@author: Caramel Koala
"""

def vor_merge(a,b):
    
    if a == 0:
        return b
    if b == 0:
        return a
    
    #get source points from a and b
    print(a)
    p_a = []
    for i in a:
        p_a.append([i[0][0],i[0][1]])
    print(p_a)
    from scipy.spatial import ConvexHull
    hull_a = ConvexHull(p_a)
    
    return 0
    
    