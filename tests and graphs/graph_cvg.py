#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 23 16:22:41 2016

@author: caramelkoala
"""

import matplotlib.pyplot as plt
import numpy as np

data = [0.00191211700439, 0.00659108161926, 6.561708450317382812e-02, 3.076887130737304688e-02, 3.304319381713867188e-01, 6.698989868164062500e-02, 5.186042070388793945e+00, 3.388028144836425781e-01, 1.773651599884033203e+01, 7.463159561157226562e-01, 5.762718605995178223e+01, 1.617437124252319336e+00, 9.475439691543579102e+01, 2.371188163757324219e+00]
tests = [10,50,100,300,500,800,1000]

c = np.zeros((2,len(tests)))
g = np.zeros((2,len(tests)))

for i in range(len(tests)):
    c[0,i] = tests[i]
    c[1,i] = data[2*i]

    g[0,i] = tests[i]
    g[1,i] = data[2*i+1]

plt.figure()

cplot, = plt.semilogy(c[0,:],c[1,:],'b',marker='o')
gplot, = plt.semilogy(g[0,:],g[1,:],'r',marker='o')
plt.legend([cplot,gplot], ['CPU execution', 'GPU execution'],loc=2)
plt.xlabel('Number of cells')
plt.ylabel('Execution time')

plt.show()

plt.figure()

cplot, = plt.plot(c[0,:],c[1,:],'b',marker='o')
gplot, = plt.plot(g[0,:],g[1,:],'r',marker='o')
plt.legend([cplot,gplot], ['CPU execution', 'GPU execution'],loc=2)
plt.xlabel('Number of cells')
plt.ylabel('Execution time')

plt.show()