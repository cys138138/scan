# -*- encoding: utf-8 -*-
from bs4 import BeautifulSoup as bs
import requests
import html5lib
import re
import random
from requests.packages.urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
import http
import time
from contextlib import closing
import os
import csv
import threading

# 设置 user-agent列表，每次请求时，可在此列表中随机挑选一个user-agnet
uas = [
    "Mozilla/5.0 (Linux; Android 5.1; OPPO A59s Build/LMY47I; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 TBS/043409 Safari/537.36 MicroMessenger/6.3.25.861 NetType/WIFI Language/zh_CN",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 10_2_1 like Mac OS X) AppleWebKit/602.4.6 (KHTML, like Gecko) Mobile/14D27 MicroMessenger/6.5.5 NetType/WIFI Language/zh_CN",
    "Mozilla/5.0 (Linux; Android 6.0.1; MI 5s Plus Build/MXB48T; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 TBS/043409 Safari/537.36 MicroMessenger/6.5.13.1100 NetType/WIFI Language/zh_CN",
    "Mozilla/5.0 (Linux; Android 5.1; F105 Build/LMY47D; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 TBS/043409 Safari/537.36 MicroMessenger/6.5.8.1060 NetType/WIFI Language/zh_CN",
    "Mozilla/5.0 (Linux; Android 7.1.1; vivo X9i Build/NMF26F; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 TBS/043409 Safari/537.36 MicroMessenger/6.5.10.1080 NetType/WIFI Language/zh_CN",
    "Mozilla/5.0 (Linux; Android 5.1; F105 Build/LMY47D; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 TBS/043409 Safari/537.36 MicroMessenger/6.5.8.1060 NetType/WIFI Language/zh_CN",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_2 like Mac OS X) AppleWebKit/603.2.4 (KHTML, like Gecko) Mobile/14F89 MicroMessenger/6.5.14 NetType/WIFI Language/zh_CN",
    "Mozilla/5.0 (Linux; Android 6.0.1; OPPO R9s Plus Build/MMB29M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 TBS/043505 Safari/537.36 MicroMessenger/6.5.13.1100 NetType/WIFI Language/zh_CN",
    "Mozilla/5.0 (Linux; Android 6.0.1; vivo Y66 Build/MMB29M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 TBS/043409 Safari/537.36 MicroMessenger/6.5.13.1100 NetType/WIFI Language/zh_CN",
    "Mozilla/5.0 (Linux; Android 5.1; OPPO R9m Build/LMY47I; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 TBS/043409 Safari/537.36 MicroMessenger/6.5.13.1100 NetType/WIFI Language/zh_CN",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 10_2_1 like Mac OS X) AppleWebKit/602.4.6 (KHTML, like Gecko) Mobile/14D27 MicroMessenger/6.5.14 NetType/4G Language/zh_CN",
    "Mozilla/5.0 (Linux; Android 6.0.1; vivo X9Plus Build/MMB29M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 TBS/043409 Safari/537.36 MicroMessenger/6.5.10.1080 NetType/WIFI Language/zh_CN",
    "Mozilla/5.0 (Linux; Android 6.0; Redmi Note 4 Build/MRA58K; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 TBS/043409 Safari/537.36 MicroMessenger/6.5.13.1100 NetType/WIFI Language/zh_CN",
    "Mozilla/5.0 (Linux; Android 5.1.1; vivo X7 Build/LMY47V; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 TBS/043409 Safari/537.36 MicroMessenger/6.5.10.1080 NetType/WIFI Language/zh_CN",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 9_2_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Mobile/13D15 MicroMessenger/6.5.12 NetType/WIFI Language/zh_CN",
    "Mozilla/5.0 (Linux; Android 4.4.4; Che1-CL10 Build/Che1-CL10; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 TBS/043409 Safari/537.36 MicroMessenger/6.5.7.1041 NetType/4G Language/zh_CN",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_3 like Mac OS X) AppleWebKit/603.3.8 (KHTML, like Gecko) Mobile/14G60 MicroMessenger/6.5.14 NetType/WIFI Language/zh_CN",
    "Mozilla/5.0 (Linux; Android 6.0; Letv X501 Build/DBXCNOP5902605181S; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 TBS/043409 Safari/537.36 MicroMessenger/6.5.4.1000 NetType/WIFI Language/zh_CN",
    "Mozilla/5.0 (Linux; Android 5.1; OPPO A37m Build/LMY47I; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 TBS/043409 Safari/537.36 MicroMessenger/6.5.13.1100 NetType/WIFI Language/zh_CN",
    "Mozilla/5.0 (Linux; Android 4.4.2; Coolpad 7605 Build/KOT49H; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 TBS/043220 Safari/537.36 MicroMessenger/6.5.6.1020 NetType/WIFI Language/zh_CN",
    "Mozilla/5.0 (Linux; Android 4.4.2; Lenovo A808t-i Build/KOT49H; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 TBS/043409 Safari/537.36 MicroMessenger/6.3.23.840 NetType/WIFI Language/zh_CN",
    "Mozilla/5.0 (Linux; Android 7.0; BLN-AL20 Build/HONORBLN-AL20; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 TBS/043409 Safari/537.36 MicroMessenger/6.5.13.1100 NetType/WIFI Language/zh_CN",
    "Mozilla/5.0 (Linux; Android 5.1.1; SM801 Build/LMY47V; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 TBS/043024 Safari/537.36 MicroMessenger/6.5.4.1000 NetType/4G Language/zh_CN",
    "Mozilla/5.0 (Linux; Android 4.4.2; 2014011 Build/HM2014011; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 TBS/043409 Safari/537.36 MicroMessenger/6.5.10.1080 NetType/WIFI Language/zh_CN",
    "Mozilla/5.0 (Linux; Android 6.0.1; vivo Y55A Build/MMB29M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 TBS/043409 Safari/537.36 MicroMessenger/6.5.10.1080 NetType/WIFI Language/zh_CN",
    "Mozilla/5.0 (Linux; Android 6.0; Le X620 Build/HEXCNFN5902606111S; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 TBS/043409 Safari/537.36 MicroMessenger/6.5.10.1080 NetType/WIFI Language/zh_CN",
    ]

def setHeader():
    randomIP = str(random.randint(0, 255)) + '.' + str(random.randint(0, 255)) + '.' + str(
        random.randint(0, 255)) + '.' + str(random.randint(0, 255))
    headers = {
        'User-Agent': random.choice(uas),
        "Accept-Language": "zh-CN,zh;q=0.8,en;q=0.6",
        'X-Forwarded-For': randomIP,
		'CLIENT-IP' : randomIP,
    }
    return headers
		
def getUrl(url):
    try:
        s = requests.Session()
        proxies = {"http": "http://47.52.5.8:3128","http":"https://1.71.110.57:80"}#proxies=proxies
        return s.get(url,headers = setHeader())
    except ConnectionResetError:
        print('ConnectionResetError')
        time.sleep(10)
        getUrl(url,stream=False)
    except http.client.IncompleteRead:
        print('http.client.IncompleteRead')
        time.sleep(10)
        getUrl(url,stream=False)		

def getPorxies():
	fp = open('proxies.txt','r')
	ips = fp.readlines()
	proxys = list()
	for p in ips:
		proxies = {'proxy':p}
		proxys.append(proxies)
	return proxys
'''
处理字符串空格和换行
'''
def dealStr(str):
	return (" "+str).strip().replace("\n", "")

'''
获取文件后缀
'''  	
def file_extension(path): 
  return os.path.splitext(path)[1]

if __name__ == "__main__":
	print('runing')
	porxiesList = getPorxies()
	proxies = random.choice(porxiesList)
	for i in range(0, 50):
		stringContent = requests.get("http://shop.xzzx24.com/proxies-url.html",headers = setHeader(),proxies=proxies)
		print(stringContent.text)
		#print(getPorxies())