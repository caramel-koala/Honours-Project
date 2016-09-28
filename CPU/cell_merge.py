# -*- coding: utf-8 -*-
"""
Created on Wed Sep 28 13:45:34 2016

@author: caramelkoala
"""

from shape import distance

def cell_merge(points,maxerror):
	best = [None, None]
	best_delta = 9000
	for p in points:
		for r in p[6]:
			newp, newerr = merge_test(p,r[1])
			delta = (p[8] + r[1][8]) - newerr
			if delta < best_delta:
				delta = best_delta
				best[0] = p
				best[1] = r
				
	
			
###############################################################################
def merge_test(p1,p2):
	
	n0 = p1[0]*p1[2] + p2[0]*p2[2]
	n1 = p1[1]*p1[2] + p2[1]*p2[2]
	d  = p1[2] + p2[2]
	
	point = [n0/d, n1/d, d]
	
	error = 0
	for source in p1:
		error += (source[2]/point[2])*distance(source,point)	
	for source in p2:
		error += (source[2]/point[2])*distance(source,point)
		
	return point,error