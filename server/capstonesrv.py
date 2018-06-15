#!/usr/bin/python
# encoding = utf-8  
import MySQLdb
import csv
import time
import sys
import socket
import thread
import hashlib
import numpy as np
reload(sys)
sys.setdefaultencoding("utf-8")


serversock = socket.socket()
host = ''
port = 3389
serversock.bind((host,port))
filename = ""
serversock.listen(10);
print "Waiting for a connection....."

clientsocket,addr = serversock.accept()
print("Got a connection from %s" % str(addr))
i=0
while True:
    i=i+1
    size = clientsocket.recv(16) # Note that you limit your filename length to 255 bytes.
    if not size:
        break
    size = int(size, 2)
    filename = clientsocket.recv(size)
    filesize = clientsocket.recv(32)
    filesize = int(filesize, 2)
    file_to_write = open(filename, 'wb')
    chunksize = 4096
    while filesize > 0:
        if filesize < chunksize:
            chunksize = filesize
        data = clientsocket.recv(chunksize)
        file_to_write.write(data)
        filesize -= len(data)

    file_to_write.close()
    print 'File received successfully'
    if i==8:
        break
serversock.close()   ###############################################

 
# loopexecute     
def insert_by_loop():
    table=[]
    with open('data.csv', 'rb') as csvfile:
        datareader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in datareader:
            table.append(row)
        table1=np.array(table)
        print type(table),type(table1),len(table)
    nrows= len(table)
    table1=np.array(table)
    nrows = len(table)
    print nrows,type(table), len(table1),type(table1)
    for i in xrange(0,nrows):
        param=[]
        try:
            sql = 'INSERT INTO capstone_table values(%s,%s,%s)'
            print 'Insert: ',table[i][0], table[i][1], table[i][2]
            param = (table[i][0], table[i][1], table[i][2])
            cur.execute(sql, param)
            conn.commit()
        except Exception as e:
            print e
            conn.rollback()
    print '[insert_by_loop execute] total:',nrows-1
#executemany  
def insert_by_many():
    table=[]
    with open('data.csv', 'rb') as csvfile:
        datareader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in datareader:
            table.append(row)
    nrows= len(table)
    param=[]
    for i in range(nrows):
        # 1col2col3col  sensor value timestamp
        param.append([table[i][0], table[i][1], table[i][2]])
    try:
        sql = 'INSERT INTO capstone_table values(%s,%s,%s)'
        cur.executemany(sql, param)
        conn.commit()
    except Exception as e:
        print e
        conn.rollback()
    print '[insert_by_many executemany] total:',nrows-1
#executemany S1_A1_E1.csv S2_A1_E1.csv S3_A1_E1.csv S4_A1_E1.csv S5_A1_E1.csv S6_A1_E1.csv S7_A1_E1.csv S8_A1_E1.csv
def insert_many():  #into database
    table1,table2,table3,table4,table5,table6,table7,table8=[],[],[],[],[],[],[],[]
    param1,param2,param3,param4,param5,param6,param7,param8=[],[],[],[],[],[],[],[]
    for i in range(1,9):
        with open('S%s_A1_E1.csv'%(i), 'rb') as csvfile:
            datareader = csv.reader(csvfile, delimiter=' ', quotechar='|')
            for row in datareader:
                if i==1:
                    table1.append(row)
                    nrow1=len(table1)
                    nrow=nrow1
                elif i==2:
                    table2.append(row)
                    nrow2=len(table2)
                    nrow=nrow2
                elif i==3:
                    table3.append(row)
                    nrow3=len(table3)
                    nrow=nrow3
                elif i==4:
                    table4.append(row)
                    nrow4=len(table4)
                    nrow=nrow4
                elif i==5:
                    table5.append(row)
                    nrow5=len(table5)
                    nrow=nrow5
                elif i==6:
                    table6.append(row)
                    nrow6=len(table6)
                    nrow=nrow6
                elif i==7:
                    table7.append(row)
                    nrow7=len(table7)
                    nrow=nrow7
                elif i==8:
                    table8.append(row)
                    nrow8=len(table8)
                    nrow=nrow8
       # for j in range(nrow2):
        for j in range(100000):
            if i==1:
                param1.append([table1[j][0]])
            elif i==2:
                param2.append([table2[j][0]])
            elif i==3:
                param3.append([table3[j][0]])
            elif i==4:
                param4.append([table4[j][0]])
            elif i==5:
                param5.append([table5[j][0]])
            elif i==6:
                param6.append([table6[j][0]])
            elif i==7:
                param7.append([table7[j][0]])
            elif i==8:
                param8.append([table8[j][0]]) 
        aparam1=np.array(param1)   
        aparam2=np.array(param2)
        aparam3=np.array(param3)
        aparam4=np.array(param4)
        aparam5=np.array(param5)
        aparam6=np.array(param6)
        aparam7=np.array(param7)
        aparam8=np.array(param8)
    print aparam8.shape,aparam2.shape,aparam3.shape,aparam4.shape,aparam5.shape    
    aparam=np.hstack((aparam1,aparam2,aparam3,aparam4,aparam5,aparam6,aparam7,aparam8))
    finalparam=aparam.tolist()
    try:
        sql = 'INSERT INTO capstone_table values(%s,%s,%s,%s,%s,%s,%s,%s)'
        cur.executemany(sql, finalparam)
        conn.commit()
    except Exception as e:
        print e
        conn.rollback()


# connect 
conn = MySQLdb.connect(host="127.0.0.1", port=3306, user="root", passwd="wzjwinner", db="capstone")
cur = conn.cursor()

# new database 
cur.execute('DROP TABLE IF EXISTS capstone_table')
sql = """CREATE TABLE capstone_table( 
        S1 CHAR(255) NOT NULL, 
        S2 CHAR(255), 
        S3 CHAR(255), 
        S4 CHAR(255), 
        S5 CHAR(255),
        S6 CHAR(255), 
        S7 CHAR(255),
        S8 CHAR(255) 
        )"""
cur.execute(sql)

# 
#table = get_table()

# loop insert
#start = time.clock()
#insert_by_loop()  
#end = time.clock()
#print '[insert_by_loop execute] Time Usage:',end-start

# executemant insert  
start = time.clock()
insert_many()
end = time.clock()
print '[insert_by_many executemany] Time Usage:',end-start


if cur:
    cur.close()
if conn:
    conn.close()


s = socket.socket()
host = ''
port = 7777
s.bind((host,port))
filename = ""
s.listen(10);
clientsocket,addr = s.accept()
print 'send to client1'
j=0
path="/root/zuihou"
while True:
    j=j+1
    filename = 'S%s_A1_E1.csv'%(j)
    size = len(filename)
    size = bin(size)[2:].zfill(16) # encode filename size as 16 bit binary
    clientsocket.send(size)
    clientsocket.send(filename)
    filename = os.path.join(path,filename)
    filesize = os.path.getsize(filename)
    filesize = bin(filesize)[2:].zfill(32) # encode filesize as 32 bit binary
    clientsocket.send(filesize)

    file_to_send=open(filename, 'rb')
    l=file_to_send.read()
    clientsocket.sendall(l)
    file_to_send.close()
    print 'File Sent %s'%(j)
    if j==8:
        break
s.close()
