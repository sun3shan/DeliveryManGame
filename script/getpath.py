# -*- coding: utf-8 -*-
"""
Created on Sun Dec  9 09:42:13 2018

@author: 01369718
"""



def getpath(start_point, end_point, walls):
    Paths = []
    if start_point['x'] > end_point['x']:
        step_x = -1
    else:
        step_x = 1
    
    if start_point['y'] > end_point['y']:
        step_y = -1
    else:
        step_y = 1   
    for x in range(start_point['x'], end_point['x']+step_x):
        path = []
        for y in range(start_point['y'], end_point['y']+step_y):
            cur_point = {'x': x, 'y': y}
            if cur_point in walls:
                return path
            else:
                getpath(cur_point, end_point, walls)