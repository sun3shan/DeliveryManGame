# -*- coding: utf-8 -*-
"""
Created on Sun Dec  9 09:08:58 2018

@author: 01369718
"""

import requests
import json
    
def http_post():
    url='http://192.168.245.130:5555/competitions'
    values ={   "name": "test80",
                "player1": "p1",
                "player2": "p2",
                "player1_host": "http://192.168.245.1:8082",
                "player2_host": "http://192.168.245.1:8084",
                "seed": 10,
                }

    jdata = json.dumps(values)             # 对数据进行JSON格式化编码
    res = requests.post(url, data=jdata)       # 生成页面请求的完整数据
    assert res.status_code == 200
    data = res.json()
    print (data)
    return


http_post()