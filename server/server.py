#!/usr/bin/python
#coding:utf-8
from multiprocessing import Process
from threading import Thread,local
import SocketServer
import subprocess
import string
import time
import MySQLdb
import csv
import time
import sys
import os
from socket import *
import hashlib
import numpy as np
#服务器读完数据后,继续读数据(不断读) 此时,抛异常Connection reset by peer
#服务器读完数据后,连续十次向客户端写数据(读完,就不停写) 此时,抛异常Broken pipe
class MyTcpServer(SocketServer.BaseRequestHandler):
#继承BaseRequestHandler基类，然后必须重写handle方法，并且在handle方法里实现与客户端的所有交互
    def handle(self):
        print "get connection from :",self.client_address           #first step
        i=0
        while True:
            try:
                i=i+1
                size = self.request.recv(16) # Note that you limit your filename length to 255 bytes.
                if not size:
                    break
                size = int(size, 2)
                filename = self.request.recv(size)
                filesize = self.request.recv(32)
                filesize = int(filesize, 2)
                file_to_write = open(filename, 'wb')
                chunksize = 4096
                while filesize > 0:
                    if filesize < chunksize:
                        chunksize = filesize
                    data = self.request.recv(chunksize)
                    file_to_write.write(data)
                    filesize -= len(data)
                file_to_write.close()
                print 'File received successfully %s'%(i)
                if i==8:
                    break
            except Exception,e:
                print "get error at:",e

        j=0
        path="/root/zuihou"
        while True:
            try:
                j=j+1
                filename = 'S%s_A1_E1.csv'%(j)
                size = len(filename)
                size = bin(size)[2:].zfill(16) # encode filename size as 16 bit binary
                self.request.sendall(size)
                self.request.sendall(filename)
                filename = os.path.join(path,filename)
                filesize = os.path.getsize(filename)
                filesize = bin(filesize)[2:].zfill(32) # encode filesize as 32 bit binary
                self.request.sendall(filesize)

                file_to_send=open(filename, 'rb')
                l=file_to_send.read()
                self.request.sendall(l)
                file_to_send.close()
                print 'File Sent %s'%(j)
                if j==8:
                    break
            except Exception,e:
                print "get error at:",e
def worker(newSocket,destAdr):
    print('build process success..')
    #local_school = local() #创建ThreadLocal对象，用来储存各线程的局部变量
    ts = Thread(target=sendfile,args=(newSocket,))
    tr = Thread(target=recvfile,args=(newSocket,))

    ts.start()
    tr.start()

    ts.join()
    tr.join()

def sendfile(newSocket):
    j=0
    path="/root/zuihou"
    while True:
        try:
            j=j+1
            filename = 'S%s_A1_E1.csv'%(j)
            size = len(filename)
            size = bin(size)[2:].zfill(16) # encode filename size as 16 bit binary
            newSocket.sendall(size)
            newSocket.sendall(filename)
            filename = os.path.join(path,filename)
            filesize = os.path.getsize(filename)
            filesize = bin(filesize)[2:].zfill(32) # encode filesize as 32 bit binary
            newSocket.sendall(filesize)
            file_to_send=open(filename, 'rb')
            l=file_to_send.read()
            newSocket.sendall(l)
            file_to_send.close()
            print 'File Sent %s'%(j)
            if j==8:
                break  
        except Exception,e:
            print "get error at:",e 
            break
    print('process2:',os.getpid())
    print('send file process over！')
 #   while True:
  #      msg = str( os.getpid())
   #     newSocket.send(msg.encode('utf8'))
    #    time.sleep(5)
def ps_is_end():
    print('子进程结束')

def recvfile(newSocket):
 #   print "get connection from :%s"%(destAdr)  #first step
    i=0
    while True:
        try:
            i=i+1
            size = newSocket.recv(16) # Note that you limit your filename length to 255 bytes.
            if not size:
                break
            size = int(size, 2)
            filename = newSocket.recv(size)
            filesize = newSocket.recv(32)
            filesize = int(filesize, 2)
            file_to_write = open(filename, 'wb')
            chunksize = 4096
            while filesize > 0:
                if filesize < chunksize:
                    chunksize = filesize
                data = newSocket.recv(chunksize)
                file_to_write.write(data)
                filesize -= len(data)
            file_to_write.close()
            print 'File received successfully %s'%(i)
            if i==8:
                break
        except Exception,e:
            print "get error at:",e
            break
    print('process1:',os.getpid())
    print('recv file process over！')
   # while True:
    #    msg = newSocket.recv(1024)
     #   if msg.decode('utf8')!= '':  #
      #      print('\r>>%s'%msg.decode('utf8'))
       # else:
        #    print('%d xiaxian'%os.getpid())
         #   newSocket.close()
          #  break

if __name__ == "__main__":
    host = ''
    port = 3389
    addr=(host,port)
    s = socket(AF_INET,SOCK_STREAM)
    s.bind((host,port))
    s.listen(5)
    SocketServer.TCPServer.allow_reuse_address = True
   # s = SocketServer.ThreadingTCPServer(addr, MyTcpServer)  #参数为监听地址和已建立连接的处理类
    print 'listening'
   # s.serve_forever()#监听，建立好TCP连接后，为该连接创建新的socket和线程，并由处理类中的handle方法处理
    while True:
        newSocket,destAdr = s.accept()
        p = Process(target=worker,args=(newSocket,destAdr,))
        p.start()
        newSocket.close()#拷贝到了新的进程中，这里的可以删掉了
    serverSocket.close()
