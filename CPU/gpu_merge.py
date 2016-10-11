#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 11 11:53:51 2016

@author: caramelkoala
"""
from numbapro import jit
import numpy as np

def gpu_merge(cells,points,err):
    e = 0
    
    ncells = np.zeros(len(cells),3)
    
    for i,c in enumerate(cells):
        c.append(points[i][7])        
        e += points[i][8]
    
#    while(True):
        
    return get_best(cells)	
        
#        if best[0] == -1:
#            print "Tesselation now singluar"
#            break
#        
#        if best[4]+e > err:
#            print "Merge criteria met"
#            print "Final Error: {0}".format(e)
#            break
#        else:
#            e += best[4]
#        
#        do_merge(best[0], best[1], best[2], best[3], ncells)
###############################################################################
@jit(target='gpu')
def get_best(cells):
    return cells