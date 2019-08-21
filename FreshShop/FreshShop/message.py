#coding:utf-8
import requests
url = "http://106.ihuyi.com/webservice/sms.php?method=Submit"
account=""
password=""
mobile=""
content=""
#定义请求的头部
headers={
    "Content-type":"application/x-www-form-urlencoded",
    "Accept":"text/plain"
}
#定义请求数据
data={
    "account":account,
    "password":password,
    "content":content,
}
response=requests.post(url,headers=headers,data=data)
    #url 请求的地址
    #head 请求头部
    #data 请求的数据
print(response.content.decode())
