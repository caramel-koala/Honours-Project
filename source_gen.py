# -*- coding: utf-8 -*-
"""
Created on Mon Jun 27 14:17:07 2016

@author: Caramel Koala
"""

def source_gen(stellar, threshold):
    source = [] 
    for i in stellar:
        if i.z > threshold:
            source.append(i)

    #source list sorted in x-axis
    #source.sort(key=lambda x: x[0])
    
    return source