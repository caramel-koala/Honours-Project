# -*- coding: utf-8 -*-
"""
Created on Wed Sep 21 10:10:37 2016

@author: caramelkoala
"""
from shape import NewPoint

def source_gen(stellar, threshold):		
	source = [] 		
	for i in stellar:		
		if i[2] > threshold:		
			source.append(NewPoint(i))		
        		
    #sort objects by x-axis
	source.sort(key=lambda x: x[1])
	source.sort(key=lambda x: x[0])
	return source 