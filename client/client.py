import socket
import os
from threading import Thread
import time

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = '139.224.236.137'
port = 3389
s.connect((host, port))
path = "/home/wangzijian/Desktop/datasource"
directory = os.listdir(path)
def sendfile(s):
    for files in directory:
        print files

        filename = files
        size = len(filename)
        size = bin(size)[2:].zfill(16) # encode filename size as 16 bit binary
        s.send(size)
        s.send(filename)

        filename = os.path.join(path,filename)
        filesize = os.path.getsize(filename)
        filesize = bin(filesize)[2:].zfill(32) # encode filesize as 32 bit binary
        s.send(filesize)

        file_to_send = open(filename, 'rb')

        l = file_to_send.read()
        s.sendall(l)
        file_to_send.close()
        print 'File Sent'
#tr = Thread(target=recvMsg,args=(s,)) 
ts = Thread(target=sendfile,args=(s,))
#tr.start()
ts.start()
#s.close()


