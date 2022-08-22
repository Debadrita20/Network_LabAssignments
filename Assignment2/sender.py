import socket
import select
import SenderSW
import ReceiverSW
import SenderGBN
import ReceiverGBN
import SenderSR
import ReceiverSR

senderList = [SenderSW,SenderGBN,SenderSR]
receiverList = [ReceiverSW,ReceiverGBN,ReceiverSR]

if __name__=='__main__':
    print('[CLIENT] : ')
    print('1.Stop and wait\n2.Go back N\n3.Selective repeat\n')
    fcpType = int(input('Enter choice(1-3): '))
    if fcpType>3 or fcpType<1:
        fcpType = 1
    fcpType -= 1
    SERVER_IP='127.0.0.1'
    SERVER_PORT=1232
    with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as client:
        client.connect((SERVER_IP, SERVER_PORT))
        msg =  client.recv(1024).decode()  
        print("From Channel :" , msg, end='')
        name=input()
        client.sendall (bytes(name,'UTF-8'))
        address = client.recv(1024).decode()
        senderAddress = int(address)
        while True:
            print('1.Send data\n2.Close\n')
            choice=int(input('Enter choice (1-2) : '))
            if choice==1:
                client.send(str.encode("request for sending"))
            elif choice==2:
                client.send(str.encode("close"))
                break
            inputs=[client]
            output=[]
            readable,writable,exceptionals=select.select(inputs,output,inputs,3600)
            for s in readable:
                data=s.recv(1024).decode()
                if data== "No client is available":
                    print(data)
                    break
                elif choice == 1:
                    file_name='test.txt'
                    receiver_list=data.split('$')
                    print('Available clients-----')
                    for index in range(0,len(receiver_list)):
                        print((index+1),'.',receiver_list[index])
                    choice=int(input('\nYour choice : '))
                    choice-=1
                    while choice not in range(0, (len(receiver_list))):
                        choice=int(input('Invalid Input...try again : '))
                        choice-=1
                    s.send(str.encode(str(choice)))
                    receiverAddress = int(s.recv(1024).decode())
                    my_sender=senderList[fcpType].Sender(client,name,senderAddress,receiver_list[index],receiverAddress,file_name)
                    my_sender.transmit()
                    data=s.recv(1024)
                    data=data.decode()
                    print(data)
            if not (readable or writable or exceptionals):
                continue
