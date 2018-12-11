# -*- coding: utf-8 -*-
"""
Created on Sun Dec  9 09:40:16 2018

@author: 01369718
"""

import numpy as np
import random
from Environment import Environment
map_shape = (12, 12)
DIR = ['U', 'D', 'L', 'R', 'S']
class Stategy:
    def __init__(self, player):
        self.state = 'init'
        self.name = player
        self.step = 0
        self.job_changed = True
    
    def gen_map(self, map_shape, jobs, walls, rival):
        self.map = np.zeros(map_shape, dtype='int')
        for wall in walls:
            self.map[wall['x'], wall['y']] = int(-1)
        self.map[rival['home_x'], rival['home_y']] = int(-1)
        for job in jobs:
            self.map[job['x'], job['y']] = int(job['value'])
            
    def update_map(self, jobs):
        if self.jobs != jobs:
            self.job_changed = True
            for job in jobs:
                self.map[job['x'], job['y']] = int(job['value'])
        else:
            self.job_changed = False
        dx = self.own['x'] - self.rival['x']
        dy = self.own['y'] - self.rival['y']
        if abs(dx) + abs(dy) == 1:
            self.map[self.rival['x'], self.rival['y']] = -1
    
    def get_info(self, jdata):
        if self.state == 'init':
            if jdata['player1']['name'] == self.name:
                self.own_player = 'player1'
                self.rival_player = 'player2'
            else:
                self.own_player = 'player2'
                self.rival_player = 'player1'
                
            self.own = jdata[self.own_player]
            self.rival = jdata[self.rival_player]
            self.own_home = (self.own['home_x'], self.own['home_y'])
            self.rival_home = (self.rival['home_x'], self.rival['home_y'])
            self.walls = jdata['walls']
            self.jobs = jdata['jobs']
            self.gen_map(map_shape, self.jobs, self.walls, self.rival)
            self.state = 'start'
        else:
            self.own = jdata[self.own_player]
            self.rival = jdata[self.rival_player]
            self.update_map(jdata['jobs'])
            self.jobs = jdata['jobs']
        self.own_cur_pos = (self.own['x'], self.own['y'])
        self.rival_cur_pos = (self.rival['x'], self.rival['y'])
        self.own_n_jobs = self.own['n_jobs']
        self.own_value = self.own['value']
        self.own_score = self.own['score']
        self.env = Environment(jdata)
        
    def path2dir(self, cur_pos, next_pos):
        dx = next_pos[0] - cur_pos[0]
        dy = next_pos[1] - cur_pos[1]
        if dx==-1 and dy==0:
            return 0
        elif dx==1 and dy==0:
            return 1
        elif dx==0 and dy==-1:
            return 2
        elif dx==0 and dy==1:
            return 3
        else:
            return 4
        
    def onStep(self, jdata):
        self.get_info(jdata)
        
        candidate = {}
        if self.own_cur_pos != self.own_home or self.own_n_jobs != 0:
            home_dist = self.env.dist[self.own_cur_pos][self.own_home]
            if home_dist>= 200 - self.step - 2 or self.own_n_jobs == 10:
                self.path = self.env.path[self.own_cur_pos][self.own_home]
                return DIR[self.path2dir(self.own_cur_pos, self.path[0])]
        
        if self.job_changed == False:
            if len(self.path)>1:
                self.path.pop(0)
                return DIR[self.path2dir(self.own_cur_pos, self.path[0])]
        for job in self.jobs:
            job_pos = (job['x'], job['y'])
            own_dist = self.AllPath[self.own_cur_pos].dist2target(job_pos)
            rival_dist = self.AllPath[self.rival_cur_pos].dist2target(job_pos)
            if own_dist<=rival_dist:
                path = self.env.path[self.own_cur_pos][job_pos]
                x_range = [node[0] for node in path]
                y_range = [node[1] for node in path]
                if not(self.own_cur_pos[0] in x_range):
                    x_range.append(self.own_cur_pos[0])
                if not(self.own_cur_pos[1] in y_range):
                    y_range.append(self.own_cur_pos[1])
                candidate[job_pos] = [(sub_job['x'], sub_job['y']) for sub_job in jobs if sub_job!=job and sub_job['x'] in x_range and sub_job['y'] in y_range]
        if len(candidate)>0:
            sorted_candidate = sorted(candidate.items(),key = lambda x:x[1],reverse = True)
            self.path = self.own_dijstra.path2target(sorted_candidate[0][0])
#            print(path)
            return DIR[self.own_dijstra.path2dir(self.own_cur_pos, self.path[0])]
        else:
            self.path = self.own_dijstra.path2target(self.own_home)
            if len(self.path)>0:
                return DIR[self.own_dijstra.path2dir(self.own_cur_pos, self.path[0])]
            else:
                print('..')
                return random.choice(DIR)
            
if __name__ == '__main__':
    data = {'player1': {'name': 'p1', 'x': 1, 'y': 6, 'home_x': 5, 'home_y': 5, 'n_jobs': 1, 'value': 12.0, 'score': 0}, 'player2': {'name': 'p2', 'x': 6, 'y': 6, 'home_x': 6, 'home_y': 6, 'n_jobs': 0, 'value': 0, 'score': 0}, 'walls': [{'x': 0, 'y': 1}, {'x': 0, 'y': 6}, {'x': 1, 'y': 1}, {'x': 1, 'y': 4}, {'x': 1, 'y': 11}, {'x': 2, 'y': 1}, {'x': 2, 'y': 7}, {'x': 2, 'y': 8}, {'x': 2, 'y': 10}, {'x': 3, 'y': 8}, {'x': 5, 'y': 1}, {'x': 6, 'y': 0}, {'x': 6, 'y': 4}, {'x': 6, 'y': 7}, {'x': 6, 'y': 10}, {'x': 7, 'y': 4}, {'x': 7, 'y': 5}, {'x': 7, 'y': 10}, {'x': 8, 'y': 1}, {'x': 9, 'y': 3}, {'x': 9, 'y': 11}, {'x': 10, 'y': 2}, {'x': 10, 'y': 8}, {'x': 11, 'y': 8}], 'jobs': [{'x': 0, 'y': 2, 'value': 7.0}, {'x': 0, 'y': 8, 'value': 9.0}, {'x': 1, 'y': 3, 'value': 6.0}, {'x': 1, 'y': 5, 'value': 6.0}, {'x': 1, 'y': 9, 'value': 10.0}, {'x': 2, 'y': 4, 'value': 8.0}, {'x': 3, 'y': 9, 'value': 10.0}, {'x': 4, 'y': 0, 'value': 8.0}, {'x': 4, 'y': 4, 'value': 6.0}, {'x': 4, 'y': 8, 'value': 7.0}, {'x': 5, 'y': 0, 'value': 8.0}, {'x': 5, 'y': 3, 'value': 7.0}, {'x': 6, 'y': 2, 'value': 10.0}, {'x': 7, 'y': 0, 'value': 11.0}, {'x': 7, 'y': 6, 'value': 10.0}, {'x': 8, 'y': 0, 'value': 12.0}, {'x': 8, 'y': 5, 'value': 12.0}, {'x': 8, 'y': 8, 'value': 10.0}, {'x': 8, 'y': 11, 'value': 9.0}, {'x': 9, 'y': 0, 'value': 7.0}, {'x': 9, 'y': 7, 'value': 10.0}, {'x': 10, 'y': 0, 'value': 12.0}, {'x': 11, 'y': 5, 'value': 7.0}, {'x': 11, 'y': 7, 'value': 12.0}]}
    mystategy = Stategy('p1')
    print(mystategy.onStep(data))
        
        