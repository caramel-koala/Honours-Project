    # -*- coding: utf-8 -*-
"""
Created on Wed Sep 28 13:45:34 2016

@author: caramelkoala
Excutes the CPU cell merge operation
"""

from shape import error

def cell_merge(points,num_facets, e):
    """
    points: the list of Voronoi facets fresh from tessellating
    num_facets: the number of desired facets
    e: the culminative distance error for the facets
    RETURNS: a_e: an array of errors for the list, also alters the list of points while merging
    """
    
    a_e = []
    
    for i in range(num_facets, len(points)):
        a_e.append(e)
        #find best merge
        best = get_best(points, e)
        
        #increase the total error by the best merge's delta
        e += best[4]
        
        #execute the best merge
        do_merge(best[0], best[1], best[2], best[3], points)
        
    print "Merge criteria met"
    print "Final Error: {0}".format(e)
        
    return a_e
###############################################################################
def get_best(points, err):
    """
    points: the list of Voronoi facets
    err: the error used as a starting point for best merge criteria and must be much higher than any possible delta
    
    RETURNS: best: the information on the best cells for merging
    """
    best = [None, None, None, None, None]
    best_delta = err*10**30
    for p in points:
         for r in p[6]:
             if r[0][6] == True:
    #test each source with it's neighbours to find it's lowest error increasing merge
                newp, newerr = merge_test(p,r[1])
                delta = newerr - (p[8] + r[1][8])
                if delta <= best_delta:
                    best_delta = delta
                    #if the best merge is better than the previous best merge, it is now the best merge
                    best = [p,r,newp,newerr, delta]

    return best
###############################################################################
def merge_test(p1,p2):
    """
    p1: the first cell to be tested for merging
    p2: the second cell to be tested for merging
    
    RETURN: point: the location of the new merged centre
            err: the error of the new merged centre
    """
    
    #find the position and magnitude of the new centre
    t  = p1[2]/float(p1[2]+p2[2])
    n0 = t*p1[0] + (1-t)*p2[0]
    n1 = t*p1[1] + (1-t)*p2[1]
    d  = t*p1[2] + (1-t)*p2[2]
        
    point = [n0, n1, d]

    #determine the distance error of the new centre relative to all it's sources
    err = 0
    for source in p1[7]:
        err += error(source,point)	
    for source in p2[7]:
        err += error(source,point)
        
    return point,err
	
###############################################################################
def do_merge(p,r,newp,newerr,points):
    """
    p: the cell in the list of cells to be moved to a new location due to merging
    r: the cell in the list of cells to be invalidated due to it's contents being merged
    newp: the new location of p due to the move
    newerr: the new error of the tessellation due to the move
    points: the list of all cells in the tessellation
    """
    
    #set the merging point to inactive
    r[0][6] = False
        
    #append the r's lines to that of p
    p[7] += r[1][7]
    #set p's error to that of the new error
    p[8] = newerr
    
    #append r's sources to that of p
    p[9] += r[1][9]
    p[9].append(r[1])
    
    #set all of r's neighbouring cells to point to p or remove them
    for rel in r[1][6]:
        if ( not rel[1][0] == p[0]) and ( not rel[1][1] == p[1]) and (rel[0][6] == True):
            p[6].append(rel)
            for r2 in rel[1][6]:
                for q in p[9]:
                    if (r2[1][0] == q[0]) and (r2[1][1] == q[1]):
                        r2[1] = p  
                if (r2[1][0] == rel[1][0]) and (r2[1][1] == rel[1][1]):
                    r2[1] = p
        else:
            rel[0][6] = False
          
    #remove r from the list of sources
    for point in points:
        if (point[0] == r[1][0]) and (point[1] == r[1][1]):
            points.remove(point)
   
    #update p to have the new values specifed by the new centre
    p[0] = newp[0]
    p[1] = newp[1]	
    p[2] = newp[2]
###############################################################################