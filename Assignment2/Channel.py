import socket
from threading import Thread, Lock
import random
import time

# address : [self connection, name, friend connection]
client_map={}


# Define the lock object
my_lock=Lock()


def inject_random_error(data):   # flips bits at random
    errdata = ''
    for i in range(len(data)):
        x = int(random.random() * 2)
        if x == 1:  # flip the bit
            if data[i] == '0':
                errdata += '1'
            else:
                errdata += '0'
        else:
            errdata += data[i]
    return errdata


def process_packet(p):
    flag=int(random.random()*10)

    if flag<=5:   # original packet sent
        return p
    elif flag<=8:  # introduce error
        return inject_random_error(p)
    else:  # introduce delay
        time.sleep(0.5)
        return p


class ConnectionThread (Thread):
    def __init__ (self, clientSocket, clientAddress):
        Thread.__init__ (self)
        self.csocket = clientSocket
        self.caddr = clientAddress
        print (clientAddress,' connected to channel')

    def setConnection (self):
        availableClients = []
        availableClientNames = []
        for address in client_map:
            if address != self.caddr and client_map[address][2] is None:
                availableClients.append(address)
                availableClientNames.append(client_map[address][1])

        if len(availableClients) == 0:
            self.csocket.send("No client is available".encode('utf-8'))
        else:
            self.csocket.send(bytes('$'.join(availableClientNames).encode('utf-8')))
            choice = int(self.csocket.recv(1024).decode())

            my_lock.acquire()
            raddr = availableClients[choice]
            
            if client_map[raddr][2] is None:
                rsocket = client_map[raddr][0]
                client_map[raddr][2] = self.caddr
                client_map[raddr][3] = 384
                client_map[self.caddr][2] = raddr
                client_map[self.caddr][3] = 576
                self.csocket.send (str(raddr[1]).encode('utf-8'))
                rsocket.send (str(self.caddr[1]).encode('utf-8'))
                print(self.caddr,"is sending data to",raddr)
            else:
                print("receiver is busy..so data cannot be sent at the moment")
            my_lock.release()

    def revokeConnection (self):
        my_lock.acquire()
        raddr = client_map[self.caddr][2]
        
        client_map[raddr][2] = None
        client_map[self.caddr][2] = None
        client_map[raddr][3] = client_map[self.caddr][3] = 1024
        self.csocket.send(str.encode("Sending completed"))
        print(self.caddr,' completed transmission of data to ',raddr)
        my_lock.release()

    # override the run method to specify the code that the thread would run on
    def run (self) -> None:
        self.csocket.send("Successfully connected to channel.\nWrite your name: ".encode('utf-8'))
        name=self.csocket.recv(1024).decode()
        self.csocket.send(str(self.caddr[1]).encode('utf-8'))
        client_map[self.caddr]=[self.csocket,name,None,1024]
        data = "open"

        while data!="close":
            inputBuffer = client_map[self.caddr][3]
            data = self.csocket.recv(inputBuffer).decode()
            if client_map[self.caddr][2] is None:
                if data == "request for sending":
                    self.setConnection()
                else:
                    pass
            else:
                rsocket = client_map[client_map[self.caddr][2]][0]
                if data == "start":
                    rsocket.send(str.encode(data))
                elif data == "end":
                    rsocket.send(str.encode(data))
                    self.revokeConnection()
                else:
                    newData = process_packet(data)
                    if newData!= '':
                        rsocket.send(str.encode(newData))
        self.csocket.close()
        print ("Client at", self.caddr, "disconnected")
        client_map.pop(self.caddr) 


if __name__=='__main__':
    SERVER_IP='127.0.0.1'
    SERVER_PORT=1232
    with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as server:
        server.setsockopt (socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((SERVER_IP,SERVER_PORT))
        server.listen(5)
        print("Channel is listening for connections")
        while True:
            conn,addr=server.accept()
            newThread = ConnectionThread (conn, addr)
            newThread.start()
