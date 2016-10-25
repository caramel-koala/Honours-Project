#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 23 17:44:43 2016

@author: caramelkoala
"""

import matplotlib.pyplot as plt
import numpy as np

f = open('gpu_profile.txt','r')

data = f.readlines()

tests = [10,50,100,300,500,800,1000]

su = np.zeros((4,len(tests)))

for i in range(len(tests)):
    su[0,i] = tests[i]
    su[1,i] = float(data[3*i])
    su[2,i] = float(data[3*i+1])
    su[3,i] = float(data[3*i+2])
    
plt.figure()
    
p1, = plt.semilogy(su[0,:], su[1,:], color='r')
p2, = plt.semilogy(su[0,:], su[2,:], color='g')
p3, = plt.semilogy(su[0,:], su[3,:], color='b')
plt.legend([p1,p2,p3], ['Data reshape', 'Data transfer', 'Merge iteration'],loc=2)
plt.xlabel('Number of cells')
plt.ylabel('Logarithmic execution time')

plt.show()