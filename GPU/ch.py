# -*- coding: utf-8 -*-
"""
Created on Wed Sep 21 11:44:06 2016

@author: caramelkoala
"""

def cross(po,pa,pb):
    return (pa[0]-po[0])*(pb[1]-po[1])-(pa[1]-po[1])*(pb[0]-po[0])
    
def amc(points,range_points):
    CH = [0]
    CH = CH*(range_points[1]-range_points[0]+1)*2
    m=0
    for i in range(range_points[0],range_points[1]+1):
        while m >= 2 and cross(CH[m-2],CH[m-1],points[i]) <= 0:
            m = m-1
        CH[m] = points[i]
        m = m+1

    t = m+1
    for i in range(((range_points[1])+1)-2,range_points[0]-1,-1):
        while m >= t and cross(CH[m-2],CH[m-1],points[i]) <= 0:
            m = m-1
        CH[m] = points[i]
        m = m+1
    m = m-1
    #print m
    for i in range(0,m):
        CH[i][5] = CH[(i-1)%m]
        CH[i][4] = CH[(i+1)%m]
    return CH