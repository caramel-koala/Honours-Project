def vorgen(source,space):

    if len(source) == 0:
        return 0
    
    #end node case: return the point with the entire space as its polygon.
    if len(source) == 1:
        return [[source[0],space]]
    
    #split the list of points into two for recusrsive voronoi.
    left = source[:len(source)/2]
    right = source[len(source)/2:]
        
    #recursively merge the cell lists back together as a single vornoi diagram.
    return vor_merge(vorgen(left,space),vorgen(right,space))
    

def vor_merge(a,b):
    
    if a == 0:
        return b
    if b == 0:
        return a
    
    #get convex hulls from a and b
    hull_a = get_hull(a)
    hull_b = get_hull(b)
    
        
    
    return 0
    
def get_hull(x):
    p_x = []
    for i in x:
        p_x.append([i[0][0],i[0][1]])
    if len(p_x)==1:
        return p_x
    else:
        from scipy.spatial import ConvexHull
        return ConvexHull(p_x)