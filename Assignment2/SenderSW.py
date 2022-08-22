import socket
import time
import threading
import PacketManager
import Analysis

defaultDataPacketSize=46
timeOut=2
analysis_file_name='SWARQ.txt'
rttStore = []


class Sender:
    def __init__(self, connection, name:str, senderAddress:int, receiver_name:str, receiverAddress:int, fileName:str):
        self.connection=connection 
        self.name = name
        self.receiver = receiver_name
        self.fileName = fileName
        self.senderAddress = senderAddress
        self.receiverAddress = receiverAddress
        self.packetType = {'data' : 0, 'ack' : 1}
        self.endTransmitting = False
        self.seqNo = 0
        self.pktCount = 0
        self.totalPktCount = 0
        self.pktSent = False
        self.sentTime = 0
        self.receiveTime = 0
        self.send_lock = threading.Lock()

    def resendPackets(self):
        time.sleep(0.2)
        while (not self.endTransmitting) or self.pktSent:
            if self.pktSent:
                current_time = time.time()
                waiting_time = (current_time-self.sentTime)
                if waiting_time > timeOut:
                    self.send_lock.acquire()
                    self.connection.send(str.encode(self.recentPacket.toBinaryString(46)))
                    self.sentTime = time.time()
                    print('Packet ',self.pktCount,' Resent')
                    self.totalPktCount += 1
                    self.send_lock.release()

    def sendData(self):
        time.sleep(0.2)
        print("\n",self.name," starts sending data to ",self.receiver,"\n")
        file = open(self.fileName,'r')
        data_frame = file.read(defaultDataPacketSize)
        self.seqNo = 0
        self.pktCount = 0
        self.totalPktCount = 0
        while data_frame:
            if not self.pktSent:
                packet = PacketManager.Packet(self.senderAddress, self.receiverAddress, self.packetType['data'], self.seqNo, data_frame)
                self.recentPacket = packet
                self.send_lock.acquire()
                self.connection.send(str.encode(packet.toBinaryString(46)))
                self.sentTime = time.time()
                self.pktSent = True
                self.seqNo = (self.seqNo+1)%2
                self.pktCount += 1
                self.totalPktCount += 1
                print("\nPacket ",self.pktCount," sent to channel")
                self.send_lock.release()
                data_frame = file.read(defaultDataPacketSize)
                if len(data_frame) == 0:
                    break
        self.endTransmitting = True
        file.close()

    def receiveAck(self):
        time.sleep(0.2)
        while (not self.endTransmitting) or self.pktSent:
            if self.pktSent:
                received = self.connection.recv(384).decode()
                packet=PacketManager.Packet.build(received)
            else:
                continue

            if packet.getType() == 1:
                if not packet.hasError():
                    if packet.seqNo == self.seqNo:
                        self.receiveTime = time.time()
                        rtt = (self.receiveTime - self.sentTime)
                        rttStore.append(rtt)
                        print("ACK ",packet.seqNo," received successfully\n")
                        self.pktSent = False 
                    else:
                        print("Wrong ACK")
                else:
                    print("ACK has error...so discarded")
            else: 
                print("Received packet is not an ACK")

    def transmit(self):
        inp=self.connection.recv(1024)
        startTime=time.time()
        sendingThread = threading.Thread(name="sendingThread", target=self.sendData)
        resendingThread = threading.Thread(name="resendingThread",target=self.resendPackets)
        ackCheckThread = threading.Thread(name='ackCheckThread', target=self.receiveAck)
        sendingThread.start()
        ackCheckThread.start()
        resendingThread.start()
        sendingThread.join()
        ackCheckThread.join()
        resendingThread.join()
        self.connection.send(str.encode("end"))
        totalTime=(time.time()-startTime)
        Analysis.storeReport(self.name, self.receiver, analysis_file_name, self.pktCount, self.totalPktCount, totalTime, rttStore)
