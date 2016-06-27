def vorgen(source,space):

    import vor_merge as vm

    if len(source) == 0:
        return 0
    
    #end node case: return the point with the entire space as its polygon.
    if len(source) == 1:
        return [[source[0],space]]
    
    #split the list of points into two for recusrsive voronoi.
    left = source[:len(source)/2]
    right = source[len(source)/2:]
        
    #recursively merge the cell lists back together as a single vornoi diagram.
    return vm.vor_merge(vorgen(left,space),vorgen(right,space))