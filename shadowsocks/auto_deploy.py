#!/usr/bin python
# -*- coding:UTF-8 -*-
#  This program is used to deploy shadowsocks！Author：Riners
import os
import json
def Getconfiguration():
    port_password={}
    num = int(input("Input the ammount of ports:"))
    Port = []
    Password = []
    for i in range(1,num+1):
        port = input("Input the %d port:" % i)
        try:
            Port.append(str(port))
            password = raw_input("Input the %d port's password:" % i)
            Password.append(password)
        except ValueError:
            print("Input port Error,try again!")
            return Getconfiguration()
    port_password=dict(zip(Port,Password))
    data = {"server":"0.0.0.0",
            "port_password":{},
            "local_port":"1080",
            "local_address":"127.0.0.1",
            "timeout":600,
            "method":"rc4-md5"
            }
    data["port_password"]=port_password.copy()
    json_str = json.dumps(data, indent=4)
    File = open("/etc/shadowsocks.json","w+")
    File.write(json_str)
def main():
    Getconfiguration()
    os.system('yum install python-setuptools && easy_install pip')
    os.system('pip install shadowsocks')
    os.system('ssserver -c /etc/shadowsocks.json -d start')
    os.system('cat /etc/shadowsocks.json')
    print("\n")
    print("Bye!")
if __name__=='__main__':
    main()