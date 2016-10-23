#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 23 15:39:01 2016

@author: caramelkoala
"""

import matplotlib.pyplot as plt
import numpy as np

merge = open('merge_error.txt','r')
vor = open('voronoi_error.txt','r')

plt.figure()

mdata = np.zeros((2,936))
vdata = np.zeros((2,936))

m = merge.readlines()
v = vor.readlines()

for x in range(936):
    mdata[0,x] = 1000-x
    mdata[1,x] = float(m[x])
    vdata[0,x] = 1000-x
    vdata[1,x] = float(v[x])
    
mplot, = plt.plot(mdata[0,:],mdata[1,:],'b')
vplot, = plt.plot(vdata[0,:],vdata[1,:],'r')
plt.legend([mplot,vplot], ['Merge cells', 'Voronoi cells'])
plt.xlabel('Number of cells')
plt.ylabel('Global Error')

plt.show()