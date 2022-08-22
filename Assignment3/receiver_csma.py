import multiprocessing
import time
import random
from NetworkLab import packet
no_senders = 4
no_receivers = 4

packet_size = 46
windowSize = 2

vulnerableTime = 0.1
propagationTime = 1
non_persistent_waiting_time = int(random.random()*2) +1
timeSlot = 0.25
collisionWaitTime = 0.1
PropagationTime = 0.8
CollisionWaitTime = 0.03


class Receiver:
    def __init__(self, name, channelToReceiver):
        self.name = name
        self.packetType = {'data': 0, 'ack': 1}
        self.senderList = dict()
        self.channelToReceiver = channelToReceiver
        self.seqNo = 0
        # self.recentACK = packet.make_packet(0,'11111111',self.name,0)

    def openFile(self, filepath):
        file = open(filepath, 'a+')
        return file

    def decodeSender(self, pkt):
        return packet.get_src_address(pkt)

    def startReceiving(self):
        while True:
            packet = self.channelToReceiver.recv()
            sender = self.decodeSender(packet)

            if sender not in self.senderList.keys():
                self.senderList[sender] = 'Received'+str(sender)+'.txt'

            ofile = self.senderList[sender]
            file = self.openFile(ofile)
            data = packet.extractData()
            file.write(data)
            file.close()
            print('RECEIVER',(self.name+1), '-->> PACKET RECEIVED')
