# -*- coding: utf-8 -*-		
"""		
Created on Mon Jun 27 14:17:07 2016		
		
@author: Caramel Koala		
"""		

from shape import Point
from operator import attrgetter
		
def source_gen(stellar, threshold):		
    source = [] 		
    for i in stellar:		
        if i.z > threshold:		
            source.append(Point(i.x,i.y,i.z))		
        		
    #sort objects by x-axis
    source.sort(key=attrgetter('x','y'))
	
        		
    return source 