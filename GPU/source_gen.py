# -*- coding: utf-8 -*-
"""
Created on Wed Sep 21 10:10:37 2016

@author: caramelkoala
"""
from operator import itemgetter
from shape import NewPoint

def source_gen(stellar, threshold):		
    source = [] 		
    for i in stellar:		
        if i[2] > threshold:		
            source.append(NewPoint(i))		
        		
    #sort objects by x-axis
    sorted(source, key=itemgetter(1,2))
	
    return source 