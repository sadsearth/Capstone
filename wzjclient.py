#!/usr/bin/python
#coding:utf-8
import socket
import sys
import time
import os
ip = '139.224.236.137'
port = 3389
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
def recvfile(filename):
    print "server ready,client recv file"
    f = open(filename, 'w')
   #f = open(filename, 'wb')
    while True:
        data = s.recv(4096)
        if data == 'EOF':
            print "recv file success!"
            break
        f.write(data)
    f.close()
def sendfile(filename):
    print "server ready,client send file"
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
        data = f.read(4096)
        if not data:
            break
        s.sendall(data)
    f.close()
    time.sleep(1)
    s.sendall('EOF')
    print "send file success!"
def writecontent():
    with open('cap.txt','w') as f0, open('capstone.txt','r') as f1:
        #for i in range(0,100):
           #f0.write('a\n')
         s=f1.read()
         f0.write(s)
        
                                
def confirm(s, client_command):
    s.send(client_command)
    data = s.recv(4096)
    if data == 'ready':
        return True
                                
try:
    s.connect((ip,port))
    while 1:
        client_command = raw_input(">>")                  #first step
        if not client_command:
            continue
                                    
        action, filename = client_command.split()
        if action == 'send':
            if confirm(s, client_command):
                writecontent()
                sendfile(filename)
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
