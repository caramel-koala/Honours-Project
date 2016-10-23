#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 23 16:40:59 2016

@author: caramelkoala
"""

import matplotlib.pyplot as plt
import numpy as np

data = [6.561708450317382812e-02, 3.076887130737304688e-02, 3.304319381713867188e-01, 6.698989868164062500e-02, 5.186042070388793945e+00, 3.388028144836425781e-01, 1.773651599884033203e+01, 7.463159561157226562e-01, 5.762718605995178223e+01, 1.617437124252319336e+00, 9.475439691543579102e+01, 2.371188163757324219e+00]
tests = [50,100,300,500,800,1000]

su = np.zeros((2,len(tests)))

for i in range(len(tests)):
    su[0,i] = tests[i]
    su[1,i] = data[2*i]/data[2*i+1]

plt.plot(g[0,:],g[1,:],'g',marker='o')
plt.xlabel('Number of cells')
plt.ylabel('Speed up')

plt.show()