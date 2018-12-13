# -*- coding: utf-8 -*-
"""
Created on Sun Dec  9 09:08:58 2018

@author: 01369718
"""

import requests
import json
import random
    
def http_post(seed):
    url='http://192.168.245.130:5555/competitions'
    values ={   "name": "test10",
                "player1": "p1",
                "player2": "p2",
                "player1_host": "http://192.168.245.1:8080",
                "player2_host": "http://192.168.245.1:8082",
                "seed": seed
                }

    jdata = json.dumps(values)             # 对数据进行JSON格式化编码
    res = requests.post(url, data=jdata)       # 生成页面请求的完整数据
    assert res.status_code == 200
    data = res.json()
    print (data)
    return

if __name__=='__main__':
#    seed = random.randint(0, 65535)
    http_post(seed)