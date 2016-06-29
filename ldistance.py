def l2_dist(a,b):
    import numpy as np
    
    d = np.sqrt((a[1]-b[1])**2 + (a[2]-b[2])**2)
    
    return d