from __future__ import absolute_import
import json
import requests
from FreshShop.celery import app

@app.task
def taskExample():
    print('send email ok!')

@app.task
def add(x=1, y=2):
    return x+y

@app.task
def DingTalk():
    url="https://oapi.dingtalk.com/robot/send?access_token=32fd3fdec07f87790e39c30c35b9020870be4405ed2a573ae3d63ef6b8d17f72"
    headers={
        "Content-Type":"application/json",
        "Chartset":"utf-8"
    }
    request_data={
        "msgtype":"text",
        "text":{
            "content":"aaa快来，和牛爷爷一起看图图的动耳神功~~"
        },
        "at":{
            "atMobiles":[

            ],

        },
        "isAtAll":True
    }
    sendData=json.dumps(request_data)
    response=requests.post(url,headers=headers,data=sendData)
    content=response.json()
    print(content)