# -*- coding: utf-8 -*-
"""
Created on Sun Dec  9 09:08:58 2018

@author: 01369718
"""

import requests
import json
import random
    
def http_post(seed):
    url='http://192.168.1.163:5555/competitions'
    values ={   "name": "test01369718-16",
                "player2": u'奇点',
                "player1": u'奇点2',
                "player2_host": "http://192.168.1.27:8080",
                "player1_host": "http://192.168.1.27:8081",
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
    http_post(3333)