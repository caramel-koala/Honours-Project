def source_gen(stellar, threshold):
    source = []   
    for i in stellar:
        if i[2] > threshold:
            source.append(i)

    #source list sorted in x-axis
    source.sort(key=lambda x: x[0])
    
    return source