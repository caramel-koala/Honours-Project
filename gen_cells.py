# -*- coding: utf-8 -*-
"""
Created on Sat Aug 13 18:01:19 2016

@author: Caramel Koala
"""
from shape import Line,Point
def gen_cells(vorspace,size):
    
    cells   = []
    
    for point in vorspace.points:
        center  = [point.x,point.y]
        lines   = []
        eps     = []
        #filters the list of lines to get only those within the space
        for rel in point.related:
            if (rel.line.avail and inspace(rel.line.p1,size) and inspace(rel.line.p2,size)):
                lines.append(rel.line)
            elif rel.line.avail and (inspace(rel.line.p1,size) or inspace(rel.line.p2,size)):
                #get those that intercept the plane
                eps.append(edgetrim(rel.line,vorspace.edge_painter,size))
        #generates list of points to make up the cell
        if len(eps) == 2:
            cells.append([center,edgecell(eps,lines,size)])
        else:
            cells.append([center,centercell(lines)])

    return cells
#generates and edge cell of the voronoi
def edgecell(eps,lines,size):
    if eps[0].p1.x == size[0] or eps[0].p1.x == 0 or eps[0].p1.y == 0 or eps[0].p1.y == size[1]:
        p1 = eps[0].p1
    else:
        p1 = eps[0].p2
        
    if eps[1].p1.x == size[0] or eps[1].p1.x == 0 or eps[1].p1.y == 0 or eps[1].p1.y == size[1]:
        p2 = eps[1].p1
    else:
        p2 = eps[1].p2
    
    if p1.x == p2.x or p1.y == p2.y:
        #there exists a staight line from p1 to p2
        lines.append(eps[0])
        lines.append(eps[1])
        lines.append(Line(p1,p2))
        return centercell(lines)
    else:
        #means it is a corner piece and a corner must be put in.
        if p1.x == 0 or p1.x == size[0]:
            p   = Point(p1.x,p2.y)
        else:
            p   = Point(p2.x,p1.y)
        lines.append(eps[0])
        lines.append(eps[1])
        lines.append(Line(p,p1))
        lines.append(Line(p,p2))
        return centercell(lines)
    
        
#generate cells fully inside the space of the voronoi 
def centercell(lines):
    results = [lines[0].p1]
    nextp   = lines[0].p2
    del lines[0]
    while True:
        nexseg  = 0
        for line in lines:
            if (line.p1 == nextp or line.p2 == nextp):
                nexseg = line
                break
        if nexseg == 0 and nextp == results[0]:
                #if it loops back to the start, we have a complete cell and we can append it
                results.append(nextp)
                #returns a list of 2-point arrays        
                return depointify(results)
        #appends the checking point to the results and moves to the next one
        if nexseg.p1 == nextp:
            results.append(nextp)
            nextp   = nexseg.p2
            lines.remove(nexseg)
        else:
            results.append(nextp)
            nextp   = nexseg.p1
            lines.remove(nexseg)
   

#checks if a point is in the plane
def inspace(p,size):
    if (p.x>=0 and p.y>=0 and p.x<=size[0] and p.y<=size[1]):
        return True
    else:
        return False

#reduces the length of edge-cutting lines to the edge     
def edgetrim(line,edges,size):
    i = getintercept(line,edges[0])
    if i == 0:
        i = getintercept(line,edges[1])
        if i == 0:
            i = getintercept(line,edges[2])
            if i == 0:
                i = getintercept(line,edges[3])
                if inspace(line.p1,size):
                    return(Line(line.p1,i))
                else:
                    return(Line(line.p2,i))
            else:
                if inspace(line.p1,size):
                    return(Line(line.p1,i))
                else:
                    return(Line(line.p2,i))           
        else:
            if inspace(line.p1,size):
                return(Line(line.p1,i))
            else:
                return(Line(line.p2,i))    
    else:
        if inspace(line.p1,size):
            return(Line(line.p1,i))
        else:
            return(Line(line.p2,i))   
            
#checks if there is an intercept between lines and if so returns it
def getintercept(l1,l2):
    #get point difference for each line
    s1_x = l1.p2.x - l1.p1.x
    s1_y = l1.p2.y - l1.p1.y
    s2_x = l2.p2.x - l2.p1.x
    s2_y = l2.p2.y - l2.p1.y
    
    s = (-s1_y * (l1.p1.x - l2.p1.x) + s1_x * (l1.p1.y - l2.p1.y)) / (-s2_x * s1_y + s1_x * s2_y)
    t = ( s2_x * (l1.p1.y - l2.p1.y) - s2_y * (l1.p1.x - l2.p1.x)) / (-s2_x * s1_y + s1_x * s2_y)

    #check for intercept and returns it
    if (s >= 0 and s <= 1 and t >= 0 and t <= 1):
        return Point(l1.p1.x + (t * s1_x), l1.p1.y + (t * s1_y))
    else:
        return 0
        
def depointify(points):
    results = []
    for point in points:
        results.append([point.x,point.y])
        
    return results