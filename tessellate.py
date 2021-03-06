# -*- coding: utf-8 -*-
"""
Created on Wed Sep 21 10:06:38 2016

@author: caramelkoala

Main function which generates the Vornoi tessellations
"""

from shape import recenter, source_to_cell, source_gen
from voronoi import Voronoi
from cell_merge import cell_merge
from gen_cells import gen_cells

###############################################################################
def tessellate(sources, planesize, num_facets, threshold=0,host=0):
    """
    sources: the list of sources to be used as facets
    planesize: the size of the plane (used to cut the lines to size once the Voronoi is formed)
    num_facets: the maximum number of facets to be generated by the final output
    threshold: the minimum pixel intensity for it to be considered a potential facet centre
    host: 0 for CPU, 1 for GPU
    """
    
    #objects above the threshold seleected
    stellars = source_gen(sources,threshold)
    print len(stellars)
    #voronoi found
    Voronoi(stellars,(0,len(stellars)-1))
    
    #append sources to cell, recentre and compute error
    source_to_cell(stellars,sources,planesize)
    recenter(stellars)
    
    e = 0
    for p in stellars:
        e += p[8]

    if (host == 0):    
        print 'cpu merge'
        e = cell_merge(stellars,num_facets, e)

    if (host == 1):
        from gpu_merge import gpu_merge
        print 'gpu merge'
        e = gpu_merge(stellars,num_facets,e, len(sources))
        
    cells = gen_cells(stellars,planesize)
        
    return cells
###############################################################################