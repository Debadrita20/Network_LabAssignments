import multiprocessing
import random
import time
import threading
from NetworkLab import errordetect
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


class Sender:
    def __init__(self, name, fileName, senderToChannel, channelToSender, collisionTechnique):
        self.recentPacket =''
        self.name = name
        self.fileName = fileName
        self.packetType = {'data': 0, 'ack': 1}
        self.dest = self.select_receiver()
        self.senderToChannel = senderToChannel
        self.channelToSender = channelToSender
        self.timeoutEvent = threading.Event()
        self.endTransmitting = False
        self.start = 0
        self.seqNo = 0
        self.pktCount = 0
        self.collisionTechnique = collisionTechnique
        self.busy = 0
        self.collisionCount = 0

    def select_receiver(self):
        return self.name

    def openFile(self, filename):
        file = open(filename, 'r')
        return file

    def send_1_persistent(self, pkt):

        while True:
            if self.busy == 0:
                file = self.openFile("collision.txt")
                collision = file.read()
                file.close()

                if collision == '1':
                    self.collisionCount += 1
                    print("SENDER{} -->> COLLISION".format(self.name + 1))
                    time.sleep(CollisionWaitTime)

                else:
                    print("SENDER{} -->> PACKET {} SENT TO CHANNEL".format(self.name + 1, self.pktCount + 1))

                    file = open('collision.txt', "w")
                    file.write(str(1))
                    file.close()

                    time.sleep(vulnerableTime)

                    file = open('collision.txt', "w")
                    file.write(str(0))
                    file.close()

                    self.senderToChannel.send(pkt)
                    time.sleep(propagationTime)
                    break

            else:
                print("SENDER{} -->> FOUND CHANNEL BUSY".format(self.name + 1))
                time.sleep(0.5)
                continue

    def send_non_persistent(self, pkt):

        while True:

            if self.busy == 0:
                file = self.openFile("collision.txt")
                collision = file.read()
                file.close()

                if collision == '1':
                    self.collisionCount += 1
                    print("SENDER{} -->> COLLISION".format(self.name + 1))
                    time.sleep(collisionWaitTime)

                else:
                    print("SENDER{} -->> PACKET {} SENT TO CHANNEL".format(self.name + 1, self.pktCount + 1))

                    file = open('collision.txt', "w")
                    file.write(str(1))
                    file.close()

                    time.sleep(vulnerableTime)

                    file = open('collision.txt', "w")
                    file.write(str(0))
                    file.close()

                    self.senderToChannel.send(pkt)
                    time.sleep(propagationTime)
                    break

            else:
                print("SENDER{} -->> FOUND CHANNEL BUSY".format(self.name + 1))
                time.sleep(non_persistent_waiting_time)
                continue

    def send_p_persistent(self, pkt):

        while True:
            if self.busy == 0:
                ch = int(random.random()*no_senders)

                if ch == 1:
                    file = self.openFile("collision.txt")
                    collision = file.read()
                    file.close()

                    if collision == '1':
                        self.collisionCount += 1
                        print("SENDER{} -->> COLLISION OCCURED".format(self.name + 1))
                        time.sleep(CollisionWaitTime)

                    else:
                        print("SENDER{} -->> PACKET {} SENT TO CHANNEL".format(self.name + 1, self.pktCount + 1))

                        file = open('collision.txt', "w")
                        file.write(str(1))
                        file.close()

                        time.sleep(vulnerableTime)

                        file = open('collision.txt', "w")
                        file.write(str(0))
                        file.close()

                        self.senderToChannel.send(pkt)
                        time.sleep(propagationTime)
                        break

                else:
                    print("SENDER{} -->> WAITING".format(self.name + 1))
                    time.sleep(timeSlot)

            else:
                print("SENDER{} -->> FOUND CHANNEL BUSY".format(self.name + 1))
                time.sleep(0.5)
                continue

    def dataIntoFrames(self):

        print("SENDER{} starts sending data to RECEIVER{}".format(self.name + 1, self.dest + 1))
        self.start = time.time()

        file = self.openFile(self.fileName)
        byte = file.read(packet_size)
        self.seqNo = 0
        while byte:
            pkt = packet.make_packet(self.seqNo,byte,self.name,self.dest)
            self.recentPacket=pkt
            if self.collisionTechnique == 1:
                self.send_1_persistent(pkt)
            elif self.collisionTechnique == 2:
                self.send_non_persistent(pkt)
            else:
                self.send_p_persistent(pkt)
            self.pktCount += 1

            byte = file.read(packet_size)
            if len(byte) == 0:
                break

        self.endTransmitting = True
        file.close()

        print("\n------------SENDER{} -->> STATS--------------".format(self.name + 1))
        print("Total packets: {}".format(self.pktCount))
        print("Total Delay:", round(time.time() - self.start, 2), "secs")
        print("Total collisions: {}".format(self.collisionCount))
        print("Throughput: {}\n".format(round(self.pktCount / (self.pktCount + self.collisionCount), 3)))

    def sense_channel(self):

        while True:
            if self.channelToSender.recv() == '1':
                self.busy = 1
            else:
                self.busy = 0

    def transmit(self):

        sendingThread = threading.Thread(name="sendingThread", target=self.dataIntoFrames())
        receivingSignalThread = threading.Thread(name="receivingSignalThread", target=self.sense_channel())

        sendingThread.start()
        receivingSignalThread.start()

        sendingThread.join()
        receivingSignalThread.join()
