import errordetect
import socket


class Receiver:
    def communicate(self,fn):
        f=open(fn,'w')
        m=''
        data = (r.recv(BUFFER_SIZE)).decode('utf-8')
        ch = int(data,2)
        data=(r.recv(BUFFER_SIZE)).decode('utf-8')
        fsize=int(data,2)
        x=1
        while True:
            data=(r.recv(BUFFER_SIZE)).decode('utf-8')
            if data=='11111111':
                break
            if ch==1:
                b=errordetect.detect_error_vrc(data)
            elif ch==2:
                b=errordetect.detect_error_lrc(data)
            elif ch==3:
                b=errordetect.detect_error_checksum(data)
            else:
                b=errordetect.detect_error_crc(data)
            if b:
                print('Error detected in packet ',x)
                m='1'
            else:
                print('No error detected in packet ',x)
                m='0'
                f.write(data[0:fsize])
            r.send(m.encode('utf-8'))
            x+=1
        f.close()


if __name__ == '__main__':
    host = socket.gethostname()
    port = 2004
    x=str(host)+str(port)
    print(x)
    a=bin(int(x))[2:]
    print(a)
    BUFFER_SIZE = 1024
    r = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    r.connect((host, port))
    obj=Receiver()
    obj.communicate('Received.txt')
    r.close()    # close connection
