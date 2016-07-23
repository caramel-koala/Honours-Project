# -*- coding: utf-8 -*-
"""
Created on Sat Jul 23 14:44:11 2016

@author: caramelkoala
"""

from shape import Line
from diagram import VD
from pointToLine import pair
from operator import attrgetter

def Voronoi(points,range_points,tangent):
    
    if (range_points[1]-range_points[0]+1) == 2:
        #print 'len = 2'
        lower = range_points[0]
        upper = range_points[1]
        line = [Line.biSector(points[lower],points[upper])]
        line[0]._p1 = points[lower]
        line[0]._p2 = points[upper]
        #hash table for point mapping to related biSector
        points[lower].related.append(pair(line[0],points[upper]))
        points[upper].related.append(pair(line[0],points[lower]))
        #Line.intersect_with_edge(line,Canvas.edge_painter,'colinear')
        vd = VD(line,range_points,points)
        return vd
    
    elif (range_points[1]-range_points[0]+1) == 3:
        #print 'len = 3'
        def clip():
            lower = range_points[0]
            upper = range_points[1]
            lines = []
            dis = []
            t = 0
            mid = []
            for i in range(lower,upper):
                for j in range(i+1,upper+1):
                    lines.append(Line.biSector(points[i],points[j]))
                    points[i].related.append(pair(lines[-1],points[j]))
                    points[j].related.append(pair(lines[-1],points[i]))
                    lines[-1]._p1 = points[i]
                    lines[-1]._p2 = points[j]
                    mid.append(((points[i]+points[j])/2,t))
                    dis.append((t,(points[i].x-points[j].x)**2+(points[i].y-points[j].y)**2,Line(points[i],points[j])))
                    t = t+1
    
            circumcenter = Line.intersect(lines[0],lines[1])
            if circumcenter is not None:
                tmp_lines = None
                dis.sort(key = lambda x : x[1])
                triangle = 'acute'
                if dis[0][1]+dis[1][1] == dis[2][1]:
                    triangle = 'right'
                    tmp_lines = dis[0:2]
                elif dis[0][1]+dis[1][1]<dis[2][1]:
                    triangle = 'obtuse'
    
                #print triangle
                s = dis[2][0]
                t = 0
    
                for i in range(lower,upper):
                    for j in range(i+1,upper+1):
                        ab = (Line(points[i],points[j]))
                        hl = Line(lines[t].p1,circumcenter)
                        result = Line.intersect(hl,ab)
    
                        #do not determine the longest side of right triangle in the same way
                        if not (triangle == 'right' and t == s):
                            if result  is  None:
                                #reverse policy for longest side of obtuse
                                if not (triangle == 'obtuse' and t == s):
                                    lines[t].p1 = circumcenter
                                else:
                                    lines[t].p2 = circumcenter
                            else:
                                if not (triangle == 'obtuse' and t == s):
                                    lines[t].p2 = circumcenter
                                else:
                                    lines[t].p1 = circumcenter
                        t = t+1
                #now determine the longest side of right triangle
                if triangle == 'right':
                    t = dis[2][0]
                    if Line.intersect(Line(lines[t].p1,circumcenter),tmp_lines[0][2])  != None or Line.intersect(Line(lines[t].p1,circumcenter),tmp_lines[1][2]) != None:
                        lines[t].p1,lines[t].p2 = circumcenter,lines[t].p2
                    else:
                        lines[t].p1,lines[t].p2 = circumcenter,lines[t].p1
    
                #create circumcenter related points
                circumcenter.iscircumcenter = True
                lines[0].connected.append(lines[1])
                lines[0].connected.append(lines[2])
                lines[1].connected.append(lines[0])
                lines[1].connected.append(lines[2])
                lines[2].connected.append(lines[0])
                lines[2].connected.append(lines[1])
    
    
            else:
                mid.sort(key = lambda s: attrgetter('x','y')(s[0]))
                t = mid[1][1]
                del_line = lines[t]
                for i in range(lower,upper+1):
                    u = points[i].related
                    for j in range(0,len(u)):
                        if u[j].line is del_line:
                            del u[j]
                            break
                del lines[t]
                #Line.intersect_with_edge(lines,Canvas.edge_painter,'colinear')
    
            return lines
    
        lines = []+clip()
        return VD(lines,range_points)
    
    elif (range_points[1]-range_points[0]+1) == 1:
        return VD([],range_points)
    else:
        mid = int((range_points[1]+range_points[0])/2)
        VDL = Voronoi(points,(range_points[0],mid),tangent)
        VDR = Voronoi(points,(mid+1,range_points[1]),tangent)
    
        merge_vd = VD.merge(VDL,VDR,tangent)
        return merge_vd