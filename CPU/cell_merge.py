    # -*- coding: utf-8 -*-
"""
Created on Wed Sep 28 13:45:34 2016

@author: caramelkoala
"""

from shape import error
#from numbapro import jit

#@jit
def cell_merge(points,err):
    e = 0
    for p in points:
        e += p[8]
    
    while(True):
        
        best = get_best(points)	
        
        if best[0] == None:
            print "Tesselation now singluar"
            break
        
        if best[4]+e > err:
            print "Merge criteria met"
            print "Final Error: {0}".format(e)
            break
        else:
            e += best[4]
        
        do_merge(best[0], best[1], best[2], best[3], points)
###############################################################################
def get_best(points):
    best = [None, None, None, None, None]
    best_delta = 99999999999
    for p in points:
         for r in p[6]:
             if r[0][6] == True:
			newp, newerr = merge_test(p,r[1])
			delta = newerr - (p[8] + r[1][8])
			if delta < best_delta:
				best_delta = delta
				best = [p,r,newp,newerr, delta]

    return best
			
###############################################################################
def merge_test(p1,p2):
    
    t = p1[2]/(p1[2]+p2[2])
    n0 = t*p1[0] + (1-t)*p2[0]
    n1 = t*p1[1] + (1-t)*p2[1]
    d = p1[2] + p2[2]
        	
    point = [n0, n1, d]

    err = 0
    for source in p1[7]:
        err += error(source,point)	
    for source in p2[7]:
        err += error(source,point)
        
    return point,err
	
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
    