# -*- coding: utf-8 -*-
"""
Created on Sun Dec  9 22:17:16 2018

@author: 01369718
"""

import numpy as np
from copy import deepcopy
import time


class Environment:
    def __init__(self, data, max_step=12, map_shape=(12,12)):
        self.map_shape = map_shape
        self.max_step = max_step
        self.map = gen_map(map_shape, data['walls'], data['player2'])
        self.path = {}
        self.dist = {}
        self.getAllPaths()

    def getAllPaths(self):
        r,c = self.map_shape
        for x in range(r):
            for y in range(c):
                if self.map[x,y]==-1:
                    continue
                else:
                    self.getPathByDijstra((x,y))
                    
    def getPathByDijstra(self, cur_pos):
#        self.map = gridmap
        r,c = self.map_shape
        self.dist[cur_pos] = np.zeros((r,c),'int')+ self.max_step + 1000
        self.dist[cur_pos][cur_pos] = 0
        self.path[cur_pos] = {}
        self.path[cur_pos][cur_pos] = []
        matrix = deepcopy(self.map)
        foo_obs = lambda x,y: matrix[int(x),int(y)]<0
        
        d = 0
        nodes = [cur_pos]
        while np.max(matrix) != -1 and d <= self.max_step:
            d += 1
            nodes = [key for key in self.path[cur_pos].keys() if matrix[key]!=-1]
            for p in nodes:
                for x,y in np.array([(0,-1),(0,1),(1,0),(-1,0)]) + p:
                    q = (x,y)
                    if x<0 or y<0 or x>=r or y>=c or foo_obs(x,y) or matrix[q] == -1:
                        continue
                    self.dist[cur_pos][q] = d
                    self.path[cur_pos][q] = deepcopy(self.path[cur_pos][p])
                    self.path[cur_pos][q].append(q)
#                    nodes.append(q)
                matrix[p] = -1
#            nodes = deepcopy(new_nodes)
                    

    def dist2target(self, cur_pos, t):
        return self.dist[cur_pos][t]

    def path2target(self, cur_pos, t):
        return self.path[cur_pos, t]


def gen_map(map_shape, walls, rival, jobs = None):
    mymap = np.zeros(map_shape, dtype='int')
    for wall in walls:
        mymap[wall['x'], wall['y']] = int(-1)
    mymap[rival['home_x'], rival['home_y']] = int(-1)
    if jobs is None:
        return mymap
    for job in jobs:
        mymap[job['x'], job['y']] = int(job['value'])
    return mymap



        
if __name__ == '__main__':
    # sim.load('maps/002.map')
    data = {'player1': {'name': 'p1', 'x': 3, 'y': 5, 'home_x': 5, 'home_y': 5, 'n_jobs': 1, 'value': 8.0, 'score': 229.0}, 'player2': {'name': 'p2', 'x': 6, 'y': 6, 'home_x': 6, 'home_y': 6, 'n_jobs': 0, 'value': 0, 'score': 0}, 'walls': [{'x': 0, 'y': 1}, {'x': 0, 'y': 6}, {'x': 1, 'y': 1}, {'x': 1, 'y': 4}, {'x': 1, 'y': 11}, {'x': 2, 'y': 1}, {'x': 2, 'y': 7}, {'x': 2, 'y': 8}, {'x': 2, 'y': 10}, {'x': 3, 'y': 8}, {'x': 5, 'y': 1}, {'x': 6, 'y': 0}, {'x': 6, 'y': 4}, {'x': 6, 'y': 7}, {'x': 6, 'y': 10}, {'x': 7, 'y': 4}, {'x': 7, 'y': 5}, {'x': 7, 'y': 10}, {'x': 8, 'y': 1}, {'x': 9, 'y': 3}, {'x': 9, 'y': 11}, {'x': 10, 'y': 2}, {'x': 10, 'y': 8}, {'x': 11, 'y': 8}], 'jobs': [{'x': 0, 'y': 0, 'value': 6.0}, {'x': 0, 'y': 2, 'value': 7.0}, {'x': 0, 'y': 8, 'value': 9.0}, {'x': 0, 'y': 9, 'value': 10.0}, {'x': 0, 'y': 10, 'value': 6.0}, {'x': 1, 'y': 3, 'value': 6.0}, {'x': 1, 'y': 5, 'value': 6.0}, {'x': 1, 'y': 9, 'value': 10.0}, {'x': 2, 'y': 0, 'value': 7.0}, {'x': 2, 'y': 4, 'value': 8.0}, {'x': 3, 'y': 0, 'value': 9.0}, {'x': 4, 'y': 0, 'value': 8.0}, {'x': 5, 'y': 0, 'value': 8.0}, {'x': 5, 'y': 10, 'value': 11.0}, {'x': 6, 'y': 3, 'value': 6.0}, {'x': 7, 'y': 6, 'value': 10.0}, {'x': 8, 'y': 11, 'value': 9.0}, {'x': 9, 'y': 4, 'value': 9.0}, {'x': 9, 'y': 5, 'value': 8.0}, {'x': 9, 'y': 10, 'value': 10.0}, {'x': 10, 'y': 10, 'value': 12.0}, {'x': 10, 'y': 11, 'value': 6.0}, {'x': 11, 'y': 4, 'value': 10.0}, {'x': 11, 'y': 11, 'value': 10.0}]}
    
    start_time = time.time()
    env = Environment(data)
    end_time = time.time()
    print(end_time - start_time)