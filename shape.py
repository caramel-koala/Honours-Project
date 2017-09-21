# -*- coding: utf-8 -*-
"""
Created on Wed Sep 21 10:17:45 2016

@author: caramelkoala

A script of utility functions for creating point and lines and performing common calculations
"""

import numpy as np

def source_gen(stellar, threshold):
    """
    Uses the complete list of sources (stellar) to select only those which are above the given threshold and returns them as the list of sources
    """
    source = []
    for i in stellar:
        if i[2] > threshold:
            source.append(NewPoint(i))
        
    #sort objects by x-axis
    source.sort(key=lambda x: x[1])
    source.sort(key=lambda x: x[0])
    return source 

def NewPoint(source):
    #uses a source to generate a voronoi centroid
    return [source[0],source[1],source[2],False,None,None,[],[],None,[]]
          #[x,y,z,circumcenter,cw,ccw,related,sources,error,consumed]

def NewLine(p1,p2):
    #uses two points to generate a line
    return [p1,p2,None,None,None,[],True]
    
def biSector(p1,p2):
    #generates the bisecting line between two points
    mid = (float(p1[0] + p2[0])/2,float(p1[1] + p2[1])/2)
    vec = vector(p1,p2)
    p1 = NewPoint(((vec[0]*( 1000000))+mid[0],(vec[1]*( 1000000))+mid[1],0))
    p2 = NewPoint(((vec[0]*(-1000000))+mid[0],(vec[1]*(-1000000))+mid[1],0))
    return NewLine(p1,p2)
    
def vector(p1,p2):
    y = p2[0]-p1[0]
    x = (p2[1]-p1[1])*-1
    return (x,y)
    
def Intersect(line1,line2):
    #finds the point of intersection between two lines
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
        t = float((y4-y3)*(x3-x1)+(x4-x3)*(y1-y3))/float((x2-x1)*(y4-y3)-(y2-y1)*(x4-x3))
        s = float((y2-y1)*(x3-x1)+(x2-x1)*(y1-y3))/float((x2-x1)*(y4-y3)-(y2-y1)*(x4-x3))
        if t >= 0 and t <= 1 and s >= 0 and s <= 1:
            x = a+b*t
            y = c+d*t
            return NewPoint((x,y,0))
        else:
            return None
    else:
        return None
								
def cross(po,pa,pb):
    #determines the ordering of points used in the divide and conquer
    return (pa[0]-po[0])*(pb[1]-po[1])-(pa[1]-po[1])*(pb[0]-po[0])
    
def amc(points,range_points):
    #generates a convex hull using Andrews Monotone Chain Algorithm
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
    
def distance(p1,p2):
    #self explanitory
    return np.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)

def wdistance(p1,p2):
    #calculates the distance based on the weighting of the intensities
    t = p1[2]/float(p1[2]+p2[2])
    return np.sqrt(t*(p1[0]-p2[0])**2 + t*(p1[1]-p2[1])**2)
    
def error(ri,rc):
    #calculates the error from source to point as a weighted distance
    return ri[2]*((ri[0]-rc[0])**2 + (ri[1]-rc[1])**2)

def source_to_cell(points, sources, size):
    #uses k-means to attach each source to it's closest voronoi centre
    for source in sources:
        min_dist = (size[1]-size[0])*(size[3]-size[2]) #starting minimum is the greatest possible distance
        minpoint = None
        
        for p in points:
            d = distance(source,p)
            if d < min_dist:
                min_dist = d
                minpoint = p
        
        minpoint[7].append(source)

def recenter(points):
    #recentres the Voronoi based on a weighted distance of all it's contained sources
    for point in points:
        numerator = [0,0]
        denomenator = 0
        for source in point[7]:
            numerator[0] += source[0]*source[2]
            numerator[1] += source[1]*source[2]
            denomenator += float(source[2])
        	
        point[0] = numerator[0]/denomenator
        point[1] = numerator[1]/denomenator
        point[2] = denomenator
        	
        err = 0
            
        for source in point[7]:
            err += error(source,point)
            
        point[8] = err