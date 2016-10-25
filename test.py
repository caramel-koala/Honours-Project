#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 21 15:39:24 2016

@author: caramelkoala
"""

import gen_cells as gc
import tesselvisual as tv
import numpy as np
from tessellate import tessellate

def test_time():
    #define the size of the plane for generality
    planesize = [600,600]
    
    tests = [50,100,300,500,800,1000]
    results = np.zeros((len(tests)*2,4))
    
    sd = 3000
    
    for i in range(len(tests)):
        #generate list of galaxies
        sources = []
        for j in range(tests[i]):
            sources.append((np.random.random()*planesize[0],np.random.random()*planesize[1],np.abs(np.random.normal(0,sd))))
        
        #error threshold
        e = sd*np.sqrt(planesize[0]*planesize[1])*tests[i]
        
        res = tessellate(sources,0,e,0,planesize)
        results[2*i,0] = tests[i]
        results[2*i,1] = res[1]
        results[2*i,2] = e
        results[2*i,3] = 0
        
        res = tessellate(sources,0,e,1,planesize)
        results[2*i+1,0] = tests[i]
        results[2*i+1,1] = res[1]
        results[2*i+1,2] = e
        results[2*i+1,3] = 1
        
    return(results)
    
def test_gpu():
    planesize = [600,600]
    
    tests = [10,50,100,300,500,800,1000]
    
    sd = 3000
    
    for i in range(len(tests)):
        #generate list of galaxies
        sources = []
        for j in range(tests[i]):
            sources.append((np.random.random()*planesize[0],np.random.random()*planesize[1],np.abs(np.random.normal(0,sd))))
        
        #error threshold
        e = sd*np.sqrt(planesize[0]*planesize[1])*tests[i]
        
        tessellate(sources,0,e,1,planesize)
        
def test_diff():
    planesize = [600,600]
    space = (((0,0),(0,planesize[1])),((0,planesize[1]),(planesize[0],planesize[1])), ((planesize[0],planesize[1]), (planesize[0],0)), ((planesize[0],0), (0,0)))
    
    sd = 3000
    
    sources = []
    for j in range(10):
        sources.append((np.random.random()*planesize[0],np.random.random()*planesize[1],np.abs(np.random.normal(0,sd))))
    
    #error threshold
    e = sd*np.sqrt(planesize[0]*planesize[1])*100
    
    res = tessellate(sources,0,e,1,planesize)
    
    print res[1]
    
    cells = gc.gen_cells(res[0],planesize,space)
    
    tv.tesselvisual(cells,sources)
    
    res = tessellate(sources,0,e,0,planesize)
    
    print res[1]
    
    cells = gc.gen_cells(res[0],planesize,space)
    
    tv.tesselvisual(cells,sources)
        
def test_gpu_max():
    planesize = [600,600]
    
    sd = 3000
    
    i = 1000
    while True:
        print i
        #generate list of galaxies
        sources = []
        for j in range(i):
            sources.append((np.random.random()*planesize[0],np.random.random()*planesize[1],np.abs(np.random.normal(0,sd))))
        
        #error threshold
        e = sd*np.sqrt(planesize[0]*planesize[1])*i
        
        tessellate(sources,0,e,1,planesize)
        
        i+=10
    
def test_error():
    
    planesize = [600,600]
    
    sd = 3000
    
    sources = []
    for j in range(1000):
        sources.append((np.random.random()*planesize[0],np.random.random()*planesize[1],np.abs(np.random.normal(0,sd))))
    
    sources.sort(key=lambda x: x[2])
    
    e = sd*np.sqrt(planesize[0]*planesize[1])*100000
    
    res = tessellate(sources,0,e,1,planesize)
    
    res2 = []
    for i in range(998):
        result = tessellate(sources,sources[i][2],e,-1,planesize)
        
        res2.append(result[2])
        
    return [res[2],res2]