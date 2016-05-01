def tesselvisual(arr_cells, arr_obj):

    #overhead
    import numpy as np
    #from scipy.spatial import Voronoi, voronoi_plot_2d
    import matplotlib.pyplot as plt
    import matplotlib
    from matplotlib.patches import Polygon
    from matplotlib.collections import PatchCollection
    
    #extract centres
    centres = []
    vert = []
    polys = []
    for cell in arr_cells:
        centres.append(cell[0])
        poly = Polygon(cell[1:],True)
        polys.append(poly)
        for v in range(1,len(cell)):
            vert.append(cell[v])
    
    ##Generate base voronoi diagram
    #vor = Voronoi(centres)
    #voronoi_plot_2d(vor) 
    
    
    #plot voronoi with polygons
    plt.figure(figsize=(20,20))
    
    p = PatchCollection(polys, cmap=matplotlib.cm.jet, alpha=0.4)

    colors = 100*np.random.rand(len(polys))
    p.set_array(np.array(colors))
    
    ax = plt.subplot()
    
    ax.add_collection(p)
    
    for v in vert:
        plt.scatter(v[0],v[1],c='r')
    
    for c in centres:
         plt.scatter(c[0],c[1],c='b',marker='+',s=100)
         
    for G in arr_obj:
        plt.scatter(G[0],G[1],c='g',s=10*np.log2(G[2]))
    
    plt.show
    return