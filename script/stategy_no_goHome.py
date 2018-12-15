# -*- coding: utf-8 -*-
"""
Created on Sun Dec  9 09:40:16 2018

@author: 01369718
"""

import numpy as np
import random
import time
from Environment import Environment
map_shape = (12, 12)
DIR = ['U', 'D', 'L', 'R', 'S']
file_name = time.strftime('%Y%m%d-%H%M%S-result.txt')
def path2dir(cur_pos, next_pos):
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
        
class Stategy:
    def __init__(self, player, jdata=None):
        global file_name
        self.state = 'init'
        self.name = player
        self.step = 0
        self.job_changed = True
        self.home_dist = 0
        self.Targets = []
        self.max_step = 200
        file_name = player+time.strftime('-%Y%m%d-%H%M%S-result.txt')
        if not(jdata is None):
            self.get_info(jdata)
    
    def gen_map(self, map_shape):
        self.map = np.zeros(map_shape, dtype='int')
        for wall in self.walls:
            self.map[wall['x'], wall['y']] = int(-1)
        self.map[self.rival['home_x'], self.rival['home_y']] = int(-1)
        for job in self.jobData:
            self.map[job['x'], job['y']] = int(job['value'])
            
    def update_map(self, jobData):
        if self.jobData != jobData:
            self.job_changed = True
            for job in jobData:
                self.map[job['x'], job['y']] = int(job['value'])
        else:
            self.job_changed = False
    
    def jobsSort(self, jobData):
        jobs = [(job['x'], job['y']) for job in jobData if self.own_env.dist[self.own_cur_pos][(job['x'], job['y'])]<1000]
        steps = dict(sorted({job: self.own_env.dist[self.own_cur_pos][job] for job in jobs}.items(), key=lambda x:x[1]))
        return tuple(steps.keys())
    
    def get_info(self, jdata):
        if self.state == 'init':
            # 判定我和对手所属玩家
            if jdata['player1']['name'] == self.name:
                self.own_player = 'player1'
                self.rival_player = 'player2'
            else:
                self.own_player = 'player2'
                self.rival_player = 'player1'
                
#            f = open(file_name, 'a')
#            f.write('Player: ' + self.own_player + '\n')
#            f.close()
            
            # 获取自己和对手的信息
            self.own = jdata[self.own_player]
            self.rival = jdata[self.rival_player]
            
            # 获取环境任两点路径
            self.own_env = Environment(jdata, self.rival)
            self.rival_env = Environment(jdata, self.own)
            
            # 获取自己和对手家的位置
            self.own_home = (self.own['home_x'], self.own['home_y'])
            self.rival_home = (self.rival['home_x'], self.rival['home_y'])
            # 获取障碍信息
            self.walls = jdata['walls']
            # 获取包裹信息
            self.jobData = jdata['jobs']
            # 生成地图
            self.gen_map(map_shape)
            # 游戏状态开始
            self.state = 'start'
            self.step = 0
        else:
            # 获取自己和对手的信息
            self.own = jdata[self.own_player]
            self.rival = jdata[self.rival_player]
            
            # 更新地图
            self.update_map(jdata['jobs'])
            # 更新包裹信息
            self.jobData = jdata['jobs']
            # 步数加1
#            self.step += 1
#            if self.own_cur_pos == (self.own['x'], self.own['y']):
            if len(self.Targets)>0:
                self.Targets[0]['step'] = self.own_env.dist[(self.own['x'], self.own['y'])][self.Targets[0]['job']]
        # 获取自己和对手位置坐标
        self.own_cur_pos = (self.own['x'], self.own['y'])
        self.rival_cur_pos = (self.rival['x'], self.rival['y'])
        
        # 判断自己是否到达第一个目标点
        if len(self.Targets)>0 and self.Targets[0]['job']==self.own_cur_pos:
            self.Targets.pop(0)
            
        # 获取地图上包裹位置，并按距离排序
        self.jobs = self.jobsSort(self.jobData)
        # 获取自己和对手包裹数
        self.own_n_jobs = self.own['n_jobs']
        self.rival_n_jobs = self.rival['n_jobs']
        
        # 获取自己得分
        self.own_value = self.own['value']
        self.own_score = self.own['score']
        
    
    def getAllTargets(self, jobs, cur_pos, residualStep=10, step = 0, level=0, value = 0):
        Target = []
        target = []
        i = 0
        for job in jobs:
            # 如果当前点——拿到包裹——回家的距离大于剩余步数，不考虑该包裹
            if self.own_env.dist[cur_pos][job] + self.own_env.dist[job][self.own_home] > residualStep or \
               (self.rival_n_jobs<10 and self.rival_env.dist[self.rival_cur_pos][job] < step + self.own_env.dist[cur_pos][job]) or \
               step>20:
                continue
            _step = step + self.own_env.dist[cur_pos][job]
            _value = value + self.map[job]
            target = [{'job': job, 'step':self.own_env.dist[cur_pos][job], 'benefit':(_value)/(_step+self.own_env.dist[job][self.own_home])}]
            if level == 0 or time.time()-self.starttime>self.limitTime:
                Target.append(target)
            else:
                subJobs = list(jobs)
                subJobs.remove(job)
                for item in self.getAllTargets(subJobs, job, residualStep - self.own_env.dist[cur_pos][job], _step, level=level-1, value=_value):
                    Target.append(list(target))
                    Target[-1].extend(item)
                Target.append(list(target))
            i += 1
        return Target   

    def onStep(self, jdata, step, level = 4, no=1, limitTime=1.0):
        self.starttime = time.time()
        self.step = step
        self.limitTime = limitTime
        self.level = level
        self.get_info(jdata)
        
        self.home_dist = self.own_env.dist[self.own_cur_pos][self.own_home]
        # n_jobs==10 and first target != home
        if self.own_n_jobs == 10 and (len(self.Targets) or (len(self.Targets)>0 and self.Targets[0]['job']!=self.own_home)):
            self.Targets = [{'job':self.own_home, 'step': self.home_dist}]
            _dir = DIR[path2dir(self.own_cur_pos, self.own_env.path[self.own_cur_pos][self.Targets[0]['job']][0])]
            return _dir
                       
        # 如果地图包裹发生变化 或 没有目标
        if self.own_cur_pos==self.own_home or self.job_changed == True or len(self.Targets)==0 or self.own_env.dist[self.own_cur_pos][self.Targets[0]['job']]>self.rival_env.dist[self.rival_cur_pos][self.Targets[0]['job']]:
            # 路径规划
            self.getPath()
            if len(self.Targets)==0:
                # n_job>0 -> goHome
                if self.own_n_jobs > 0:
                    self.Targets = [{'job':self.own_home, 'step': self.own_env.dist[self.own_cur_pos][self.own_home]}]
                # go the nearest job
                else:
                    self.Targets = [{'job':self.jobs[0], 'step':self.own_env.dist[self.own_cur_pos][self.jobs[0]]}]
                
        if len(self.Targets)>0 and self.Targets[0]['job']!=self.own_home and \
           self.own_cur_pos!=self.own_home and \
           (self.own_env.dist[self.own_cur_pos][self.Targets[0]['job']] == self.own_env.dist[self.own_cur_pos][self.own_home] +self.own_env.dist[self.own_home][self.Targets[0]['job']]):           

            self.Targets.insert(0, {'job':self.own_home, 'step': self.own_env.dist[self.own_cur_pos][self.own_home]})
        
        # 计算方向
        _dir = DIR[path2dir(self.own_cur_pos, self.own_env.path[self.own_cur_pos][self.Targets[0]['job']][0])]
        
        return _dir
    
    def canIGoHome(self):
        
        # 获取从家可以拿到的所有目标可能, 并得到收益
        Targets = self.getAllTargets(self.jobs, self.own_home, self.max_step-self.step-self.home_dist, level = min(self.level, 10))
        Benefit = [target[-1]['benefit'] for target in Targets]
        if len(Benefit)>0:
            maxBenefit = max(Benefit)
            newTargets = Targets[Benefit.index(maxBenefit)]
            new_benefit = np.sqrt((self.own_value)/(self.home_dist) * maxBenefit)
            old_benefit = (self.own_value + sum([self.map[target['job']] for target in newTargets]))/(sum([target['step'] for target in self.Targets])+self.own_env.dist[newTargets[-1]['job']][self.own_home])
            if new_benefit > old_benefit:
                self.Targets = newTargets
                self.Targets.insert(0, {'job':self.own_home, 'step': self.home_dist})
            
    
    def getPath(self):
        if self.step == 0:
            level = 4
        else:
            level = self.level
        # 获取地图获取level个包裹的所有走法和步数
        Targets = self.getAllTargets(self.jobs, self.own_cur_pos, self.max_step-self.step, level = min(level, 10-self.own_n_jobs))
        
        Benefit = [target[-1]['benefit'] for target in Targets]
        
        if len(Benefit)>0:
            maxBenefit = max(Benefit)
            self.Targets = Targets[Benefit.index(maxBenefit)]
         
            
        
            
if __name__ == '__main__':
    data = {'player1': {'name': 'p1', 'x': 3, 'y': 5, 'home_x': 5, 'home_y': 5, 'n_jobs': 0, 'value': 0, 'score': 573.0}, 'player2': {'name': 'p2', 'x': 8, 'y': 8, 'home_x': 6, 'home_y': 6, 'n_jobs': 1, 'value': 12.0, 'score': 667.0}, 'walls': [{'x': 0, 'y': 1}, {'x': 0, 'y': 6}, {'x': 1, 'y': 1}, {'x': 1, 'y': 4}, {'x': 1, 'y': 11}, {'x': 2, 'y': 1}, {'x': 2, 'y': 7}, {'x': 2, 'y': 8}, {'x': 2, 'y': 10}, {'x': 3, 'y': 8}, {'x': 5, 'y': 1}, {'x': 6, 'y': 0}, {'x': 6, 'y': 4}, {'x': 6, 'y': 7}, {'x': 6, 'y': 10}, {'x': 7, 'y': 4}, {'x': 7, 'y': 5}, {'x': 7, 'y': 10}, {'x': 8, 'y': 1}, {'x': 9, 'y': 3}, {'x': 9, 'y': 11}, {'x': 10, 'y': 2}, {'x': 10, 'y': 8}, {'x': 11, 'y': 8}], 'jobs': [{'x': 0, 'y': 0, 'value': 6.0}, {'x': 0, 'y': 3, 'value': 8.0}, {'x': 0, 'y': 5, 'value': 7.0}, {'x': 0, 'y': 8, 'value': 8.0}, {'x': 0, 'y': 10, 'value': 6.0}, {'x': 0, 'y': 11, 'value': 7.0}, {'x': 1, 'y': 2, 'value': 12.0}, {'x': 1, 'y': 7, 'value': 8.0}, {'x': 1, 'y': 8, 'value': 10.0}, {'x': 1, 'y': 10, 'value': 8.0}, {'x': 2, 'y': 2, 'value': 6.0}, {'x': 4, 'y': 0, 'value': 12.0}, {'x': 5, 'y': 0, 'value': 8.0}, {'x': 6, 'y': 2, 'value': 8.0}, {'x': 6, 'y': 11, 'value': 12.0}, {'x': 7, 'y': 3, 'value': 6.0}, {'x': 7, 'y': 11, 'value': 9.0}, {'x': 8, 'y': 0, 'value': 8.0}, {'x': 8, 'y': 6, 'value': 9.0}, {'x': 10, 'y': 0, 'value': 12.0}, {'x': 10, 'y': 5, 'value': 10.0}, {'x': 10, 'y': 11, 'value': 10.0}, {'x': 11, 'y': 3, 'value': 9.0}, {'x': 11, 'y': 11, 'value': 7.0}]}
    mystategy = Stategy('p1')
    starttime = time.time()
    step  = 1
    print(mystategy.onStep(data, step-1, 7, 2, 1.0))
    endtime = time.time()
    print(endtime-starttime)
        
        