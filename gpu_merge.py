#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 11 11:53:51 2016

@author: caramelkoala
"""
from numba import cuda
import numpy as np
###############################################################################
def gpu_merge(points,err,numobj):
    
    #reshape points for gpu
    centre = np.zeros((len(points),4))
    related = np.zeros((len(points),len(points)/2+1))
    sources = np.zeros((numobj,3))
    
    #populate arrays for gpu
    for i,p in enumerate(points): 
        centre[i,0] = p[0]
        centre[i,1] = p[1]
        centre[i,2] = p[2]
        centre[i,3] = p[8]
        for j,r in enumerate(p[6]):
            if r[0][6]==True:
                for k in xrange(len(points)):
                    if (points[k][0]==r[1][0]) and (points[k][1]==r[1][1]):
                        related[i,j] = k
                        break
                else: related[i,j] = -1
        for o in p[7]:
            sources[i,0] = o[0]
            sources[i,1] = o[1]
            sources[i,2] = o[2]
            

    results = np.zeros((len(points)))
    
    #transfer arrays to gpu
    d_results = cuda.to_device(results)
    d_centre = cuda.to_device(centre)
    d_related = cuda.to_device(related)
    d_sources = cuda.to_device(sources)
    
    p = len(points)
    #get grid and block sizes
    b = 32
    g = len(points)/b + 1
        
    #call kernel
    g_get_best[g,b](d_centre,p,d_results,d_related,d_sources)
    
    results = d_results.copy_to_host()
    
    print results
###############################################################################
@cuda.jit
def g_get_best(centre,p,results,related,sources):
    #get x,y coords in GPU
    x,y = cuda.grid(2)
    
    #check if in array range
    if x < p:
        results[x] = centre[x,0] + centre[x,1] + centre[x,2]