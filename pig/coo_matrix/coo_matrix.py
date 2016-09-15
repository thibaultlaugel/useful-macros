@outputSchema("out:{(position:int, column:chararray)}")
def getMappingColumns(values, blacklisted):
    bl = blacklisted.split(',')
    return [(pos, i) for pos, i in enumerate(sorted(list(set([v[0] for v in values]) - set(bl))))]

@outputSchema("header:chararray")
def getHeader(values, columns, blacklisted):
    col = columns.split(',')
    l = getMappingColumns(values, blacklisted)
    return ','.join(list(col) + [i[1] for i in l])

@outputSchema("header:chararray")
def getMatrix(mapping, values):
    map_ = dict((y, x) for x,y in mapping)
    arr_ = ['0'] * len(map_)
    for v in values:
        try:
            idx = map_[v[0]]
            val = v[1]
            arr_[idx] = str(val)
        except KeyError:
            pass
    return ','.join(arr_)
