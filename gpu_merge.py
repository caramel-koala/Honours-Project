#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 11 11:53:51 2016

@author: caramelkoala
"""
from numba import cuda, float32
import numpy as np
import time
###############################################################################
def gpu_merge(points,err,numobj):
    
    start = time.time()
    #reshape points for gpu
    centre = np.zeros((len(points),4))
    related = np.zeros((len(points),len(points)),dtype='int32')
    sources = np.zeros((len(points),numobj,3))
    
    e = 0 #global error
    a_e = []
    #populate arrays for gpu
    for i,p in enumerate(points): 
        centre[i,0] = p[0]
        centre[i,1] = p[1]
        centre[i,2] = p[2]
        centre[i,3] = p[8]
        e += p[8]
        for j,r in enumerate(p[6]):
            if r[0][6]==True:
                for k in xrange(len(points)):
                    if (points[k][0]==r[1][0]) and (points[k][1]==r[1][1]):
                        related[i,j] = k
                        break
                else: related[i,j] = -1
        for j in range(len(p[6]),len(points)/2+1):
            related[i,j] = -2
        for j,s in enumerate(p[7]):
            sources[i,j,0] = s[0]
            sources[i,j,1] = s[1]
            sources[i,j,2] = s[2]
    end = time.time()   
    print 'reshape time: {0}'.format(end-start)
    
    start = time.time()
    #transfer arrays to gpu
    d_results = cuda.device_array((len(points),7),np.float32)
    d_centre = cuda.to_device(centre)
    d_related = cuda.to_device(related)
    d_sources = cuda.to_device(sources)
    end = time.time()
    print 'transfer time: {0}'.format(end-start)
     
    p = len(points)
    #get grid and block sizes
    b = 32
    g = len(points)/b + 1
        
    start = time.time()
    while(True):
        #call kernel
        d_get_best[g,b](d_centre,p,d_results,d_related,d_sources,err,numobj)
        
        results = d_results.copy_to_host()
        
        a_e.append(e)
        
        best = np.array([0,0,0,0,0,0,err])
        for r in range(results.shape[0]):
            if results[r,6] < best[6]:
                for q in range(7):
                    best[q] = results[r,q]
        
        if best[6]+e > err:
            print "Merge criteria met"
            print "Final Error: {0}".format(e)
            break
        else:
            e += best[6]

        h_do_merge(best,points)
        d_best = cuda.to_device(best)
        d_do_merge[g,b](d_best,d_centre,d_related,d_sources,p,numobj,err)
    end = time.time()   
    print 'compute time: {0}'.format(end-start)
    
    return(a_e)
###############################################################################
@cuda.jit
def d_get_best(centre,p,results,related,sources,err,n):
    #get x,y coords in GPU
    x,y = cuda.grid(2)
    
    #check if in array range
    if x < p:
        
        best = cuda.local.array(7,float32)
        test = cuda.local.array(7,float32)
        best[6] = err
        test[5] = x
        
        for r in range(p):
            r0 = related[x,r]
            if r0 == -2: break
            if (r0 != -1) and (r0 != x):
                d_merge_test(x,r0,centre,sources,test,n)
                test[6] = test[3] - (centre[x,3] + centre[r0,3])
                if (test[6] < best[6]):
                    for q in range(7):
                        best[q] = test[q]
                    
        for q in range(7):
            results[x,q] = best[q]
                
###############################################################################
@cuda.jit(device=True)
def d_merge_test(x,r,centre,sources,test,n):
    if (centre[x,0] == centre[r,0]) and (centre[x,1] == centre[r,1]):
        return
        
    t = centre[x,2]/(centre[x,2]+centre[r,2])
    test[0] = t*centre[x,0] + (1-t)*centre[r,0]
    test[1] = t*centre[x,1] + (1-t)*centre[r,1]
    test[2] = centre[x,2] + centre[r,2]
    
    e = 0
    for s in range(n):
        e += sources[x,s,2]*((sources[x,s,0]-test[0])**2 + (sources[x,s,1]-test[1])**2)
        e += sources[r,s,2]*((sources[r,s,0]-test[0])**2 + (sources[r,s,1]-test[1])**2)
        if (sources[r,s,2] == 0) and (sources[x,s,2] == 0):
            break #i.e. if both list of sources have reached their end.
    
    test[3] = e

    test[4] = r
###############################################################################
def h_do_merge(best,points):
	
    p = points[(int)(best[5])]
    r = points[(int)(best[4])]
    
    for rel in p[6]:
        if (rel[1][0] == r[0]) and (rel[1][1] == r[1]):
            rel[0][6] = False
            break
        	
    p[7] += r[7]
    p[8] = best[3]		
    
    p[9] += r[9]
    p[9].append(r)
  
    
    for i in xrange(len(points)):
        if (points[i][0] == r[0]) and (points[i][1] == r[1]):
            points[i] = p
    
    for rel in r[6]:
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

    p[0] = best[0]
    p[1] = best[1]	
    p[2] = best[2] 
###############################################################################
@cuda.jit
def d_do_merge(best,centre,related,sources,p,n,err):
    
    #get x,y coords in GPU
    x,y = cuda.grid(2)
    
    #check if in array range
    if x < p:
        
        for i in range(p):
            if related[x,i] == -2:
                break
            if related[x,i] == best[4]:
                related[x,i] = best[5]

    if x == best[5]:
        centre[x,0] = best[0]
        centre[x,1] = best[1]
        centre[x,2] = best[2]
        centre[x,3] = best[3]

        r = (int)(best[4])

        for i in range(n):
            if (sources[x,i,2] == 0):
                for j in range(n-i):
                    if (sources[r,j,2] == 0):
                        break
                    sources[x,i+j,0] = sources[r,j,0]
                    sources[x,i+j,1] = sources[r,j,1]
                    sources[x,i+j,2] = sources[r,j,2]
                break
            
    if x == best[4]:
        centre[x,0] = err
        centre[x,1] = err
        centre[x,2] = err
        centre[x,3] = 0
         