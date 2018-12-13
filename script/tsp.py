# -*- coding: utf-8 -*-
"""
Created on Wed Dec 12 10:13:13 2018

@author: andy
"""

from subsetGenerator import subsetGenerator

class Graph(object):
    def __init__(self, dictIn):
        self.graph = dictIn
        
    def dist(self, x, y):
        return self.graph[(x,y)]

def minRange(graph, d, target):
    tupleList = list(target[0])
    tupleList.remove(target[1])
    sublist = tupleList
    min = 1000;
    prev_best = list();
    size = len(sublist)
    for i in range(size):
        temp = (tuple(sublist), sublist[i])
        curr = d[temp][0] + graph.dist(target[1], sublist[i]);
        if curr < min:
            min = curr;
            prev_best = list(temp);
    return (min, tuple(prev_best));
    

def tsp(graph, n):
    d = dict()
    kRange = range(n+1);
    kRange.remove(0)
    kRange.remove(1)
    
    for k in kRange:
        d[((k,),k)] = (graph.dist(k, 1), 0);
    
    sRange = range(n + 1);
    sRange.remove(0);
    sRange.remove(1);
    for s in sRange:
        subsetList = subsetGenerator(sRange, s)
        for subset in subsetList:
            for i in range(s):
                temp = (tuple(subset), subset[i]);
                d[temp] = minRange(graph, d, temp);
    min = 10000;
    for j in kRange:
        temp1 = d[(tuple(kRange), j)];
        curr = temp1[0];
        if curr < min:
            min = curr;
            best = temp1
            lastpoint = j
    print('minimum value', min)
    
    l = [lastpoint]
    step = n - 2
    i = 0
    while i < step :
        l.append(best[1][1])
        best = d[best[1]]
        i += 1
        
    return l

def buildGraph(points, dist):
    d = dict();
    size = len(points)
    iRange = range(size + 1);
    iRange.remove(0);
    for i in iRange:
        j = i + 1
        while j <= size:
            d[(i, j)] = dist[(i,j)];
            d[(j, i)] = d[(i, j)];
            j += 1
    return Graph(d)        
    
def tsp_interface(points, dist):
    graph = buildGraph(points, dist)
    sequence = tsp(graph, len(points))
    
    return sequence
        
        
        
        
        
        