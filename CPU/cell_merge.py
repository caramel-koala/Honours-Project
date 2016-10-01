    # -*- coding: utf-8 -*-
"""
Created on Wed Sep 28 13:45:34 2016

@author: caramelkoala
"""

from shape import wdistance

def cell_merge(points):
	for i in xrange(10):
		
		best = get_best(points)		
		
		do_merge(best[0], best[1], best[2], best[3], points)
		
		
###############################################################################
def get_best(points):
    best = [None, None, None, None]
    best_delta = 900000
    for p in points:
         for r in p[6]:
             if r[0][6] == True:
			newp, newerr = merge_test(p,r[1])
			delta = newerr - (p[8] + r[1][8])
			if delta < best_delta:
				best_delta = delta
				best = [p,r,newp,newerr]

    return best
			
###############################################################################
def merge_test(p1,p2):
    
    t = p1[2]/(p1[2]+p2[2])
    n0 = t*p1[0] + (1-t)*p2[0]
    n1 = t*p1[1] + (1-t)*p2[1]
    d  = p1[2] + p2[2]
        	
    point = [n0, n1, d]

    error = 0
    for source in p1[7]:
        error += wdistance(source,point)	
    for source in p2[7]:
        error += wdistance(source,point)
        
    return point,error
	
###############################################################################
def do_merge(p,r,newp,newerr,points):
	
    p[0] = newp[0]
    p[1] = newp[1]	
    p[2] = newp[2]
     
    r[0][6] = False
        	
    p[7] += r[1][7]
    p[8] = newerr		
    
    p[9] += r[1][9]
    p[9].append(r[1])
    
    for i in xrange(len(points)):
        if (points[i][0] == r[1][0]) and (points[i][1] == r[1][1]):
            points[i] = p
         
    for rel in r[1][6]:
        if (( not rel[1][0] == p[0]) and ( not rel[1][1] == p[1])) and (rel[0][6] == True):
            p[6].append(rel)
        else:
            rel[0][6] = False
        for r2 in rel[1][6]:
            if (r2[1][0] == rel[1][0]) and (r2[1][1] == rel[1][1]):
                r2[1] = p
            for q in p[9]:
                if (r2[1][0] == q[0]) and (r2[1][1] == q[1]):
                    r2[1] = p     
    