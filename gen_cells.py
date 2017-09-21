# -*- coding: utf-8 -*-
"""
Created on Wed Sep 21 19:12:50 2016

@author: caramelkoala

#generate a list of ordered points which determine the cells boundaries
"""

def gen_cells(points,size):
    """
    points: the complete voronoi structure with all facets interlinked due to the dulaney graph
    size: the dimensions of the plane to be mapped to, must be rectangular
    
    RETURNS: cells: the simplified Voronoi structure
    """

    cells   = []
    
    for point in points:
        cont = True
        for cell in cells:
            if cell[0][0] == point[0] and cell[0][1] == point[1] and cell[0][2] == point[2]:
                cont = False
                break
        if not cont:
            continue
        center  = (point[0],point[1],point[2])
        lines   = []
        #filters the list of lines to get only those within the space
        for rel in point[6]:
            if (rel[0][6]):
                lines.append(rel[0])
        if len(lines)==0:
            print "no cell for source {0}".format(center)
            continue
        else:
            cells.append([center,centercell(lines, size)])
					
    return cells

#checks if a point is in the plane
def outside(p,size):
    if (p[0]>=size[0] and p[1]>=size[2] and p[0]<=size[1] and p[1]<=size[3]):
        return False
    else:
        return True

#generate cells fully inside the space of the voronoi 
def centercell(lines, size):
    results = [lines[0][0]]
    nextp   = lines[0][1]
    del lines[0]
    while True:
        if nextp == results[0]:
                #if it loops back to the start, we have a complete cell and we can append it
                results.append(nextp)
                #returns a list of 2-point arrays        
                return depointify(results)
        nexseg  = 0
        for line in lines:
            if (line[0] == nextp or line[1] == nextp):
                nexseg = line
                break
        
        #if it is a divergent edge cell
        if nexseg == 0:
            if outside(nextp, size):
                found = False
                for line in lines:
                    if outside(line[0], size):
                        results.append(nextp)
                        results.append(line[0])
                        nextp   = line[1]
                        lines.remove(line)
                        found = True
                        break
                    elif outside(line[1], size):
                        results.append(nextp)
                        results.append(line[1])
                        nextp   = line[0]
                        lines.remove(line)
                        found = True
                        break
                if found:
                    continue
                else:
                    results.append(nextp)
                    nextp = results[0]
                    continue
            else:
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
