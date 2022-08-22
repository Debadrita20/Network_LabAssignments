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
    print('Choose flow-control protocol :-')
    print('1.Stop and wait\n2.Go back N\n3.Selective repeat\n')
    fcpType = int(input('Enter your choice (1-3) :'))
    if fcpType>3 or fcpType<1:
        fcpType = 1
    fcpType -= 1
    SERVER_IP='127.0.0.1'
    SERVER_PORT=1232
    with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as client:
        client.connect((SERVER_IP, SERVER_PORT))
        msg =  client.recv(1024).decode()
        print("From channel :" , msg, end='')
        name=input()
        client.sendall (bytes(name,'utf-8'))
        address = client.recv(1024).decode()
        senderAddress = int(address)
        while True:
            print('1.Receive data\n2.Close\n')
            choice=int(input('Enter choice : '))
            if choice!=1:
                client.send(str.encode("close"))
                break
            inputs=[client]
            output=[]
            # Wait until any input/output event or timeout occurs
            readable,writable,exceptionals=select.select(inputs,output,inputs,3600)
            for s in readable:
                data=s.recv(1024).decode()
                if data== "No client is available":
                    print(data)
                    break
                elif choice == 1:
                    print('Receiving data-----')
                    file_name=''
                    if fcpType == 0:
                        file_name='SWARQ_rec.txt'
                    elif fcpType == 1:
                        file_name='GBN_rec.txt'
                    else:
                        file_name='SR_rec.txt'
                    receiverAddress = int(data)
                    s.send (bytes("start", 'utf-8'))
                    my_receiver=receiverList[fcpType].Receiver(client,name,senderAddress,receiverAddress,file_name)
                    my_receiver.startReceiving()
            if not (readable or writable or exceptionals):
                continue
