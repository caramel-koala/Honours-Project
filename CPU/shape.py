# -*- coding: utf-8 -*-
"""
Created on Wed Sep 21 10:17:45 2016

@author: caramelkoala
"""
def NewPoint(source):
    return [source[0],source[1],source[2],False,None,None,[],[],None]

def NewLine(p1,p2):
    return [p1,p2,None,None,None,[],True]
    
def biSector(p1,p2):
    mid = ((p1[0] + p2[0])/2,(p1[1] + p2[1])/2)
    vec = vector(p1,p2)
    p1 = NewPoint(((vec[0]*(100000))+mid[0],(vec[1]*(100000))+mid[1],0))
    p2 = NewPoint(((vec[0]*(-100000))+mid[0],(vec[1]*(-100000))+mid[1],0))
    return NewLine(p1,p2)
    
def vector(p1,p2):
    y = p2[0]-p1[0]
    x = (p2[1]-p1[1])*-1
    return (x,y)
    
def Intersect(line1,line2):
    x1 = line1[0][0]
    y1 = line1[0][1]
    x2 = line1[1][0]
    y2 = line1[1][1]

    x3 = line2[0][0]
    y3 = line2[0][1]
    x4 = line2[1][0]
    y4 = line2[1][1]

    a = x1
    b = x2-x1
    c = y1
    d = y2-y1

    f = x4-x3
    h = y4-y3
    if b*h-d*f != 0:
        t = ((y4-y3)*(x3-x1)+(x4-x3)*(y1-y3))/((x2-x1)*(y4-y3)-(y2-y1)*(x4-x3))
        s = ((y2-y1)*(x3-x1)+(x2-x1)*(y1-y3))/((x2-x1)*(y4-y3)-(y2-y1)*(x4-x3))
        if t >= 0 and t <= 1 and s >= 0 and s <= 1:
            x = a+b*t
            y = c+d*t
            return NewPoint((x,y,0))
        else:
            return None
    else:
        return None
								
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

    for i in range(0,m):
        CH[i][5] = CH[(i-1)%m]
        CH[i][4] = CH[(i+1)%m]
    return CH