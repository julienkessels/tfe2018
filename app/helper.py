import collections
from operator import itemgetter

def reduce(input):
    d=collections.defaultdict(int)
    a=[]
    b=[]
    for key,val in input:
        if not key.lower() in a: a.append(key.lower())
        d[key.lower()]+=val
    for f in a:
        b.append((f,d[f]))
    return b
