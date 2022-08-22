import socket

if __name__=='__main__':
    host = socket.gethostname()
    port = 2004  # port for FTP server
    BUFFER_SIZE = 1024
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    name=input('Enter the name of the file needed:')
    s.send(name.encode('utf-8'))
    data=s.recv(BUFFER_SIZE).decode('utf-8')
    print('The file received:')
    print(data)
    s.close()