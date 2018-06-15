import socket
import os
from threading import Thread

s = socket.socket()
host = '139.224.236.137'
port = 3389
s.connect((host, port))

def recvfile(s):
    i=0
    while 1:
        i=i+1
        size = s.recv(16) # Note that you limit your filename length to 255 bytes.
        if not size:
            break
        size = int(size, 2)
        filename = s.recv(size)
        filesize = s.recv(32)
        filesize = int(filesize, 2)
        file_to_write = open('S%s_A1_E1.csv'%(i), 'wb')
        chunksize = 4096
        while filesize > 0:
            if filesize < chunksize:
                chunksize = filesize
            data = s.recv(chunksize)
            file_to_write.write(data)
            filesize -= len(data)

        file_to_write.close()
        print 'File received successfully %s'%(i)
        if i==8:
            break

#ts = Thread(target=sendMsg,args=(s,)) 
tr = Thread(target=recvfile,args=(s,))
#ts.start()
tr.start()
#s.close()
