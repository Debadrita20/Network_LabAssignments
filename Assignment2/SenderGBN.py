import socket
import random
import time
import threading
import PacketManager
import Analysis

MAX_WINDOW_SIZE = 7
defaultDataPacketSize=46
timeOut=2
analysis_file_name='GBN_analysis.txt'
rttStore = []


class Sender:
    def __init__(self, connection, name:str, senderAddress:int, receiver_name:str, receiverAddress:int ,fileName:str): 
        self.connection = connection
        self.name = name
        self.receiver = receiver_name
        self.fileName = fileName
        self.senderAddress = senderAddress
        self.receiverAddress = receiverAddress
        self.packetType = {'data' : 0, 'ack' : 1}
        self.timeoutEvent = threading.Event()
        self.endTransmitting = False
        self.front = 0
        self.end = 0
        self.window_size = 0
        self.pktCount = 0
        self.totalPkt = 0
        self.current_window = []
        self.packet_timer = []
        for index in range(0,8):
            self.current_window.append(0)
            self.packet_timer.append(0)
        self.window_write_lock  = threading.Lock()

    def validACK(self,ack_no:int):
        if (self.front < ack_no <= self.end) or (self.end < self.front < ack_no) or (ack_no <= self.end < self.front):
            return True
        else:
            return False

    def resendPackets(self):
        time.sleep(0.2)
        while (not self.endTransmitting) or (self.window_size>0):
            if self.window_size>0:
                current_time = time.time()
                front_waiting_time = (current_time-self.packet_timer[self.front])
                if front_waiting_time > timeOut:
                    self.window_write_lock.acquire()
                    temp=self.front
                    while temp!=self.end:
                        self.connection.send(str.encode(self.current_window[temp].packet))
                        print('Packet ',temp,' Resent')
                        self.packet_timer[temp] = time.time()
                        temp=((temp+1)%(MAX_WINDOW_SIZE+1))
                        self.totalPkt += 1
                    self.window_write_lock.release()

    def sendData(self):
        time.sleep(0.2)
        print("\n",self.name," starts sending data to ",self.receiver,"\n")
        file = open(self.fileName,'r')
        data_frame = file.read(defaultDataPacketSize)
        while data_frame:
            if self.window_size<MAX_WINDOW_SIZE:
                packet = PacketManager.Packet(self.senderAddress, self.receiverAddress, self.packetType['data'], self.end, data_frame)
                self.current_window[self.end] = packet
                self.window_write_lock.acquire()
                self.connection.send(str.encode(packet.toBinaryString(46)))
                print("\nPacket ",self.end," Sent")
                self.packet_timer[self.end] = time.time()
                self.end = ((self.end+1)%(MAX_WINDOW_SIZE+1))
                self.window_size += 1
                self.pktCount += 1
                self.totalPkt += 1
                data_frame = file.read(defaultDataPacketSize)
                self.window_write_lock.release()
            if len(data_frame) == 0:
                break
        self.endTransmitting = True
        file.close()

    def receiveAck(self):
        time.sleep(0.2)
        while (not self.endTransmitting) or (self.window_size>0):
            if self.window_size>0:
                received = self.connection.recv(384).decode()
                packet=PacketManager.Packet.build(received)
            else:
                continue
            if packet.getType() == 1:
                if not packet.hasError():
                    if self.validACK(packet.seqNo):
                        self.window_write_lock.acquire()
                        while self.front!=packet.seqNo:
                            rtt = (time.time() - self.packet_timer[self.front])
                            rttStore.append(rtt)
                            print("Packet ",self.front," has reached successfully\n")
                            self.front = ((self.front+1)%(MAX_WINDOW_SIZE+1))
                            self.window_size -= 1
                        self.window_write_lock.release()
                    else:
                        print("ACK is wrong...so discarded")
                else:
                    print("ACK has error...so discarded")
            else: 
                print("Received packet is not an ACK")

    def transmit(self):
        inp=self.connection.recv(1024)
        startTime = time.time()
        sendingThread = threading.Thread(name="sendingThread", target=self.sendData)
        ackCheckThread = threading.Thread(name='ackCheckThread', target=self.receiveAck)
        resendingThread = threading.Thread(name="resendingThread",target=self.resendPackets)
        sendingThread.start()
        ackCheckThread.start()
        resendingThread.start()
        sendingThread.join()
        ackCheckThread.join()
        resendingThread.join()
        self.connection.send(str.encode("end"))
        totalTime=(time.time()-startTime)
        Analysis.storeReport(self.name, self.receiver, analysis_file_name, self.pktCount, self.totalPkt, totalTime, rttStore)
