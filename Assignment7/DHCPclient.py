import socket

if __name__=='__main__':
    host=socket.gethostname()
    port=2014  # for the server
    BUFFER_SIZE=1024
    s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    s.sendto('Request for IP Address'.encode('utf-8'),(host,port))
    data,addr=s.recvfrom(BUFFER_SIZE)
    print('Have been assigned address ',data.decode('utf-8'))
    s.sendto('Address accepted'.encode('utf-8'),(host,port))
    ack,addr2=s.recvfrom(BUFFER_SIZE)
    print(ack.decode('utf-8'))
