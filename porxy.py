# -*- encoding: utf-8 -*-
import requests
import os
from bs4 import BeautifulSoup
os.chdir(r'E:\workSpace\python')
headers = {'User-Agent':'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Mobile Safari/537.36'}
url = 'http://www.xicidaili.com/nn/1'
s = requests.get(url,headers = headers)
print(s.text)


soup = BeautifulSoup(s.text,'html5lib')
ips = soup.select('#ip_list tr')
fp = open('host.txt','w')
for i in ips:
    try:
        ipp = i.select('td')
        ip = ipp[1].text
        host = ipp[2].text
        fp.write(ip)
        fp.write('\t')
        fp.write(host)
        fp.write('\n')
    except Exception as e :
        print ('no ip !')
fp.close()