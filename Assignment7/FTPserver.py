import socket

if __name__=='__main__':
    TCP_IP = '0.0.0.0'
    TCP_PORT = 2004
    BUFFER_SIZE = 1024
    while True:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((TCP_IP, TCP_PORT))
        print('Listening for a client')
        s.listen(5)
        (conn, (ip, port)) = s.accept()
        print('Connected with a client')
        filename=conn.recv(BUFFER_SIZE).decode('utf-8')
        print('Client is requesting for file ',filename)
        f=open(filename,'r')
        data=f.read()
        conn.send(data.encode('utf-8'))
        s.close()
        ch=input('Do you wish to terminate the server process? Enter Y if so, otherwise press any other key: ')
        if ch=='y' or ch=='Y':
            break
