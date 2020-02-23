#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This program is used to get China's IP address!   Author: Riners
import re
from urllib import request
def Getip():
    MatchIpv4 = re.compile(r'apnic\|CN\|ipv4\|(.*)\|(.*)\|(.*)\|allocated')
    f1 = open('result.txt','w')
    url = "http://ftp.apnic.net/apnic/stats/apnic/delegated-apnic-latest"
    for i in request.urlopen(url):
        i = i.decode('GBK')
        if MatchIpv4.findall(i):
            result = MatchIpv4.sub(func, i)
            '''利用func中返回的结果替换字符串i中匹配到的结果'''
            print (result)
            f1.write(result)
def func(m):
    return m.group(1) + "/" + str(32 - Mylog2(m.group(2)))
def Mylog2(num):
    num = int(num)
    x = 0
    while num > 1:
        num >>= 1
        x += 1
    return x
if __name__ == '__main__':
    Getip()