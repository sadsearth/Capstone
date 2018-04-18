#!/usr/bin/python
#coding:utf-8
import socket
import sys
import time
import os
from datetime import datetime
import pytz
import csv
import random

ip = '139.224.236.137'
port = 3389
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
def recvfile(filename):
    print "server ready,client recv file!"
    f = open(filename, 'w')
   #f = open(filename, 'wb')
    while True:
        data = s.recv(1024)    #4096 before   bufsize参数是说的每次接收的最大的长度，而不是一定接收这么长。
        if data == 'EOF':
            print "recv file success!"
            break
        f.write(data)
    f.close()
def sendfile(filename):
    print "server ready,client send file!"
    f = open(filename, 'r')
   #f = open(filename, 'rb')
    #f = open('/home/wangzijian/Desktop/test.txt', 'r')
    #f = open('wangzijian.txt', 'rb+')     
    #f = open('wj.txt', 'w')
   # f=open('/home/wangzijian/Desktop/cap.txt','w+')
  #  f.write('wangzijian')
    #for i in range(0,100):
    #f.write('a')
    #f.close()
    while True:
        data = f.read(1024)
        if not data:
            break
        s.sendall(data)
    f.close()
    time.sleep(2)       #############
    s.sendall('EOF')
    print "send file success!"
def writecontent():
    with open('data.csv','a') as f0, open('capstone.txt','r') as f1:
        #for i in range(0,100):
           #f0.write('a\n')
	 # 文件头，一般就是数据名
	 
         fileHeader = ["sensors", "value", "timestamp"]

         writer = csv.writer(f0)
         tz = pytz.timezone('Europe/Helsinki')
	 t = datetime.fromtimestamp(int(time.time()), pytz.timezone('Europe/Helsinki')).strftime('%Y-%m-%d %H:%M:%S %Z%z')
         print(t)
         d1 = ["EMG-1", random.randint(1,254), t]
         d2 = ["EMG-2", random.randint(1,254), t]
         d3=["EMG-3", random.randint(1,254), t]
         d4=["EMG-4", random.randint(1,254), t]
         d5 = ["EMG-5", random.randint(1,254), t]
         d6 = ["EMG-6", random.randint(1,254), t]
         d7 = ["EMG-7", random.randint(1,254), t]
         d8 = ["EMG-8", random.randint(1,254), t]
         d9=["EMG-9", random.randint(1,254), t]
         d10=["EMG-10", random.randint(1,254), t]
         d11 = ["EMG-11", random.randint(1,254), t]
        #s=f1.read()
	 # 写入的内容都是以列表的形式传入函数
	 if i==0:
 	     writer.writerow(fileHeader)
	 else:
	     writer.writerow(d1)
	     writer.writerow(d2)
	     writer.writerow(d3)
	     writer.writerow(d4)
	     writer.writerow(d5)
	     writer.writerow(d6)
	     writer.writerow(d7)
	     writer.writerow(d8)
	     writer.writerow(d9)
	     writer.writerow(d10)
	     writer.writerow(d11)

		# f0.write(t)
        
                                
def confirm(s, client_command):
    s.send(client_command)
    data = s.recv(1024)
    if data == 'ready':
        return True
                                
try:
    s.connect((ip,port))
    #while 1:
    #client_command = raw_input(">>")                  #first step
    client_command = 'send data.csv'	
    action, filename = client_command.split()
    i=0 
    while 1:	  
        if action == 'send':           
	    if confirm(s, client_command):
	        writecontent()
                print time.time()                   #0.4s/time
		sendfile(filename)            
                time.sleep(2)	  ######################	
		i=i+1
	    else:
		print "server get error!"
	elif action == 'recv':
	    if confirm(s, client_command):
		recvfile(filename)
	    else:
	        print "server get error!"
	else:
	    print "command error!"
except socket.error,e:
    print "get error as",e
finally:
    s.close()
