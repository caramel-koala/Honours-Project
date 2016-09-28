# -*- coding: utf-8 -*-
"""
Created on Wed Sep 28 13:45:34 2016

@author: caramelkoala
"""

from shape import distance

def cell_merge(points):
	for i in xrange(1):
		
		best = get_best(points)		
		
		do_merge(best[0], best[1], best[2], best[3])
		
		
###############################################################################
def get_best(points):
	best = [None, None, None, None]
	best_delta = 900000
	for p in points:
		if p[9] == True:
			for r in p[6]:
				if r[0][6] == True:
					newp, newerr = merge_test(p,r[1])
					delta = (p[8] + r[1][8]) - newerr
					if delta < best_delta:
						best_delta = delta
						best = [p,r,newp,newerr]
						
	return best
			
###############################################################################
def merge_test(p1,p2):
	
	n0 = (p1[0] + p2[0])/2
	n1 = (p1[1] + p2[1])/2
	d  = p1[2] + p2[2]
	
	point = [n0, n1, d]
	
	error = 0
	for source in p1[7]:
		error += distance(source,point)	
	for source in p2[7]:
		error += distance(source,point)
		
	return point,error
	
###############################################################################
def do_merge(p,r,newp,newerr):
	
	p[0] = newp[0]
	p[1] = newp[1]	
	p[2] = newp[2]
				
	r[0][6] = False
	
	p[6] += r[1][6]
	
	p[7] += r[1][7]
	p[8] = newerr		
	
#	r[1][0] = p[0]	
#	r[1][1] = p[1]	
#	r[1][2] = p[2]	
#	r[1][3] = p[3]	
#	r[1][4] = p[4]	
#	r[1][5] = p[5]	
#	r[1][6] = p[6]	
#	r[1][7] = p[7]	
#	r[1][8] = p[8]	
#	r[1][9] = False