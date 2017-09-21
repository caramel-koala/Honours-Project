# -*- coding: utf-8 -*-
"""
Created on Wed Sep 21 19:41:52 2016

@author: caramelkoala

Uses matplotlib to visualise the tessellations
"""

def tesselvisual(arr_cells, arr_obj, size):
    
    """
    arr_cells: List of completed voronoi cells (only centres and lines, no interconnections)
    arr_objects: Lists of all sources to be displayed to show how they were used to form the Voronoi
    size: planesize which is used to show the actual window
    """

    #overhead
    import numpy as np
    import matplotlib.pyplot as plt
    import matplotlib.cm
    from matplotlib.patches import Polygon
    from matplotlib.collections import PatchCollection
    import math
    
    #extract centres
    centres = []
    rcentres = []
    polys = []
    for cell in arr_cells:
        if not cell[1] == None:
            centres.append(cell[0])
            poly = Polygon(cell[1],True)
            polys.append(poly)
        else:
            rcentres.append(cell[0])
    
    
    #plot voronoi with polygons
    plt.figure()
    
    p = PatchCollection(polys, cmap=matplotlib.cm.jet, alpha=0.4)

    colors = 255*np.random.rand(len(polys))
    p.set_array(np.array(colors))
    
    ax = plt.subplot()
    
    ax.add_collection(p)
    
    print len(arr_obj)
    for G in arr_obj:
        plt.scatter(G[0],G[1],c='b',marker='o',s=math.sqrt(G[2]))
    
    for c in centres:
         plt.scatter(c[0],c[1],c='r',marker='*',s=100)
         
    for r in rcentres:
         plt.scatter(r[0],r[1],c='k',marker='*',s=100)
    
    plt.axis(size)
    plt.savefig('plot.png')