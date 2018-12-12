# -*- coding: utf-8 -*-
"""
Created on Mon Dec 10 23:21:33 2018

@author: 01369718
"""

import asyncio
#import sys
from sanic import Sanic
from sanic import response
import time
import random
from stategy import Stategy


step = 0
myname = 'p2'
app = Sanic(__name__)


@app.route('/start',methods=["POST"])
async def on_start(request):
    global step, mystategy, json
    mystategy = Stategy(myname)
    json = request.json
    print('game start')
    step = 0
    return response.json({})

@app.route('/step',methods=["POST"])

async def on_step(request):
    global step, mystategy, json, mydir
    json = request.json
    step += 1
    if step%10 == 0:
        print(step)
#    return response.json({'action':'S'})
    try:
        starttime = time.time()
        mydir = mystategy.onStep(json,9)
        print(time.time()-starttime) #random.choice(['S','S','S','S','S'])
        return response.json({'action':mydir})
    except:
        mydir = mystategy.onStep(json)
        return response.json({'action':mydir})
        

@app.route('/end',methods=["POST"])
async def on_end(request):
    global step, myname, json
    result = [u'平局', u'获胜', u'失败']
    json = request.json
    win = int(0)
    if json['player1']['score'] > json['player2']['score']:
        win = int(1)
    elif json['player1']['score'] < json['player2']['score']:
        win = int(-1)
    if json['player1']['name'] != myname:
        win = -win
    print(result[win]+': '+ str(json['player1']['score']) + ' - ' + str(json['player2']['score']))
    return response.json({})

def main():
#	seed = int(sys.argv[1])
#	seed = int(100)
#	random.seed(seed)
	app.run(host='0.0.0.0', port=8084)

if __name__ == '__main__':
    main()