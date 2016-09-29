# -*- coding: utf-8 -*-
"""
Created on Wed Sep 21 19:41:52 2016

@author: caramelkoala
"""

def tesselvisual(arr_cells, arr_obj):

    #overhead
    import numpy as np
    import matplotlib.pyplot as plt
    import matplotlib
    from matplotlib.patches import Polygon
    from matplotlib.collections import PatchCollection
    
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

    colors = 100*np.random.rand(len(polys))
    p.set_array(np.array(colors))
    
    ax = plt.subplot()
    
    ax.add_collection(p)
    
    
    for G in arr_obj:
        plt.scatter(G[0],G[1],c='g',s=G[2]*10)
    
    for c in centres:
         plt.scatter(c[0],c[1],c='b',marker='+',s=100)
         
    for r in rcentres:
         plt.scatter(r[0],r[1],c='r',marker='+',s=100)
    
    plt.show