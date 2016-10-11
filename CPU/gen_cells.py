# -*- coding: utf-8 -*-
"""
Created on Wed Sep 21 19:12:50 2016

@author: caramelkoala
"""

import shape as sh

def gen_cells(points,size,space):
    
    cells   = []
    
    for point in points:
        center  = (point[0],point[1],point[2])
        lines   = []
        eps     = []
        #filters the list of lines to get only those within the space
        for rel in point[6]:
            if (rel[0][6] and inspace(rel[0][0],size) and inspace(rel[0][1],size)):
                lines.append(rel[0])
            elif rel[0][6] and (inspace(rel[0][0],size) or inspace(rel[0][1],size)):
                #get those that intercept the plane
                eps.append(edgetrim(rel[0],space,size))
                #generates list of points to make up the cell
        if len(eps) == 2:
            cells.append([center,edgecell(eps,lines,size)])                    
        else:
            if len(lines)==0:
                continue
            else:
                cells.append([center,centercell(lines)])
					
    return cells


#checks if a point is in the plane
def inspace(p,size):
    if (p[0]>=0 and p[1]>=0 and p[0]<=size[0] and p[1]<=size[1]):
        return True
    else:
        return False

#reduces the length of edge-cutting lines to the edge     
def edgetrim(line,edges,size):
    i = sh.Intersect(line,edges[0])
    if i == None:
        i = sh.Intersect(line,edges[1])
        if i == None:
            i = sh.Intersect(line,edges[2])
            if i == None:
                i = sh.Intersect(line,edges[3])
                if inspace(line[0],size):
                    return(sh.NewLine(line[0],i))
                else:
                    return(sh.NewLine(line[1],i))
            else:
                if inspace(line[0],size):
                    return(sh.NewLine(line[0],i))
                else:
                    return(sh.NewLine(line[1],i))           
        else:
            if inspace(line[0],size):
                return(sh.NewLine(line[0],i))
            else:
                return(sh.NewLine(line[1],i))    
    else:
        if inspace(line[0],size):
            return(sh.NewLine(line[0],i))
        else:
            return(sh.NewLine(line[1],i))   

#generates and edge cell of the voronoi
def edgecell(eps,lines,size):
    if eps[0][0][0] == size[0] or eps[0][0][0] == 0 or eps[0][0][1] == 0 or eps[0][0][1] == size[1]:
        p1 = eps[0][0]
    else:
        p1 = eps[0][1]
        
    if eps[1][0][0] == size[0] or eps[1][0][0] == 0 or eps[1][0][1] == 0 or eps[1][0][1] == size[1]:
        p2 = eps[1][0]
    else:
        p2 = eps[1][1]
    
    if p1[0] == p2[0] or p1[1] == p2[1]:
        #there exists a staight line from p1 to p2
        lines.append(eps[0])
        lines.append(eps[1])
        lines.append(sh.NewLine(p1,p2))
        return centercell(lines)
    else:
        #means it is a corner piece and a corner must be put in.
        if (size[0]-p1[0] < size[0]-p2[0] and size[0]-p1[0] < size[0]/1000.0) or (p1[0] < p2[0] and p1[0] < size[0]/1000.0):
            p   = sh.NewPoint((p1[0],p2[1],0))
        else:
            p   = sh.NewPoint((p2[0],p1[1],0))
        lines.append(eps[0])
        lines.append(eps[1])
        lines.append(sh.NewLine(p,p1))
        lines.append(sh.NewLine(p,p2))
        return centercell(lines)					

#generate cells fully inside the space of the voronoi 
def centercell(lines):
    results = [lines[0][0]]
    nextp   = lines[0][1]
    del lines[0]
    while True:
        nexseg  = 0
        for line in lines:
            if (line[0] == nextp or line[1] == nextp):
                nexseg = line
                break
        if nexseg == 0 and nextp == results[0]:
                #if it loops back to the start, we have a complete cell and we can append it
                results.append(nextp)
                #returns a list of 2-point arrays        
                return depointify(results)
        if nexseg == 0:
            return None
        #appends the checking point to the results and moves to the next one
        if nexseg[0] == nextp:
            results.append(nextp)
            nextp   = nexseg[1]
            lines.remove(nexseg)
        else:
            results.append(nextp)
            nextp   = nexseg[0]
            lines.remove(nexseg)
   
#converts list of points to a list of lists      
def depointify(points):
    results = []
    for point in points:
        results.append([point[0],point[1]])
        
    return results
