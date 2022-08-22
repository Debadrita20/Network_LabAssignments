from random import random

import errordetect
import channel
import socket


class Sender:
    def __init__(self,ip,port):
        self.ip=ip
        self.port=port

    def communicate(self,fn,fsize,ch):
        f=open(fn,'r')
        s=f.read()
        f.close()
        if len(s)%fsize !=0:
            st='0'*(fsize-(len(s)%fsize))
            s=s+st
        i=0
        count=0
        tcount=0
        m=bin(ch)[2:]
        conn.send(m.encode('utf-8'))
        m=bin(fsize)[2:]
        conn.send(m.encode('utf-8'))
        while i<len(s):
            if ch==1:
                m=errordetect.vrc(s[i:(i + fsize)])
            elif ch==2:
                m=errordetect.lrc(s[i:(i + fsize)])
            elif ch==3:
                m=errordetect.checksum(s[i:(i + fsize)])
            elif ch==4:
                m= errordetect.crc(s[i:(i + fsize)])
            print('Original Packet:',m)
            m2=channel.inject_error(m)
            print('Packet Sent    :',m2)
            conn.send(m2.encode('utf-8'))
            d=conn.recv(BUFFER_SIZE)
            er=d.decode('utf-8')
            if m2!=m and er=='1':
                count+=1
            if m!=m2:
                tcount+=1
            i=i+fsize
        m='11111111'
        conn.send(m.encode('utf-8'))
        print('Percentage of errors detected:',(count*100)/tcount)


if __name__=="__main__":
    TCP_IP = '0.0.0.0'
    TCP_PORT = 2004
    x=TCP_IP.replace('.','')+str(TCP_PORT)
    print(x)
    print(bin(int(x))[2:])
    BUFFER_SIZE = 1024
    file=input('Enter the name of the file:')
    fsize=8*int(input('Enter the number of bytes for dataword:'))
    while True:
        print('Enter 1 for VRC error detection scheme')
        print('Enter 2 for LRC error detection scheme')
        print('Enter 3 for Checksum error detection scheme')
        print('Enter 4 for CRC error detection scheme')
        ch=int(input('Enter your choice:'))
        if 1 <= ch <= 4:
            break
        print('Invalid Input!!!Enter a valid number')
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((TCP_IP, TCP_PORT))
    s.listen(5)
    (conn, (ip, port)) = s.accept()
    obj=Sender(ip,port)
    obj.communicate(file,fsize,ch)

