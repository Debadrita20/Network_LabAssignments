import socket
import random

if __name__=='__main__':
    UDP_IP=socket.gethostname()
    UDP_PORT=2014
    BUFFER_SIZE=1024
    address_list=[]
    i=1
    while True:
        s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        s.bind((UDP_IP,UDP_PORT))
        print('Listening for a client')
        data,addr=s.recvfrom(BUFFER_SIZE)
        print('Received request from a client')
        add=''
        changed=True
        while changed:
            add = '192.168.0.' + str(int(random.random() * 200))
            changed=False
            for ad in address_list:
                if ad[1]==add:     # if generated address is already in the list
                    add = '192.168.0.' + str(int(random.random() * 200))  # generate new address
                    changed=True  # address has been changed, so have to check the list again

        s.sendto(str(add).encode('utf-8'),addr)
        acc,addr2=s.recvfrom(BUFFER_SIZE)
        if acc.decode('utf-8')=='Address accepted':
            address_list.append(('Client '+str(i),add))
            i=i+1
            s.sendto('Address added to the ARP Cache'.encode('utf-8'),addr)
        print('ARP Cache Contents currently:')
        for ad in address_list:
            print(ad)
        ch = input('Do you wish to terminate the server process? Enter Y if so, otherwise press any other key: ')
        if ch == 'y' or ch == 'Y':
            break





