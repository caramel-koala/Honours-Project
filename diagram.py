# -*- coding: utf-8 -*-
"""
Created on Sat Aug 06 22:01:37 2016

@author: Caramel Koala
"""
###############################################################################   
def merge(left,right):
    return left
    
###############################################################################    
#Calculate biisector
def biSector(p1,p2):
    mid = [(p1[0]+p2[0])/2,(p1[1]+p2[1])/2]
    m   = -(p1[0]-p2[0])/float(p1[1]-p2[1])
    return  [mid,m] #return midpoint and gradient of bisector
###############################################################################