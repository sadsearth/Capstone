#!/usr/bin/python
#coding:utf-8
import SocketServer
import subprocess
import string
import time
import socket
class MyTcpServer(SocketServer.BaseRequestHandler):  
#继承BaseRequestHandler基类，然后必须重写handle方法，并且在handle方法里实现与客户端的所有交互
    def recvfile(self, filename):
        print "starting reve file!"
        f = open(filename, 'wb')
        self.request.send('ready')
        while True:
            data = self.request.recv(4096)
            if data == 'EOF':
                print "recv file success!"
                break
            f.write(data)
        f.close()
                                       
    def sendfile(self, filename):
        print "starting send file!"
        self.request.send('ready')
        time.sleep(1)
        f = open(filename, 'rb')
        while True:
            data = f.read(4096)
            if not data:
                break
            self.request.send(data)
        f.close()
        time.sleep(1)
        self.request.send('EOF')
        print "send file success!"
                                   
    def handle(self):
        print "get connection from :",self.client_address           #first step
        while True:
            try:
                data = self.request.recv(4096)  #接收4096字节数据
                print "recv client_command:", data         # get data: recv/send test.txt data is client_command
                if not data:
                    print "break the connection!"
                    break                
                else:
                    action, filename = data.split()
                    if action == "send":
                        self.recvfile(filename)
                    elif action == 'recv':
                        self.sendfile(filename) 
                    else:
                        print "get error!"
                        continue
            except Exception,e:
                print "get error at:",e
                                           
                                       
if __name__ == "__main__":
    host = ''
    port = 3389
    SocketServer.TCPServer.allow_reuse_address = True
    s = SocketServer.ThreadingTCPServer((host,port), MyTcpServer)
    s.serve_forever()
