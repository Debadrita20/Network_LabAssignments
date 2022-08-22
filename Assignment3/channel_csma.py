import threading
import time
from NetworkLab import packet
import random

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


class Channel:
    def __init__(self, senderToChannel, channelToSender, receiverToChannel, channelToReceiver):

        self.senderToChannel = senderToChannel
        self.channelToSender = channelToSender
        self.receiverToChannel = receiverToChannel
        self.channelToReceiver = channelToReceiver
        self.busy = False

    def channelizePktFromSenderToReceiver(self):

        while True:
            pkt = self.senderToChannel.recv()
            self.busy = True
            time.sleep(PropagationTime)
            self.busy = False
            receiver = packet.get_dest_address(pkt)
            self.channelToReceiver[receiver].send(pkt)

    def send_busy_signal(self, sender):
        while True:
            if self.busy:
                self.channelToSender[sender].send(str(1))  # busy
            else:
                self.channelToSender[sender].send(str(0))  # idle

    def start_channel(self):

        print("\nCHANNEL is running")
        channelToReceiverThreadList = []
        channelToSenderThreadList = []
        sender = 0

        t = threading.Thread(name='PktThread' + str(sender + 1), target=self.channelizePktFromSenderToReceiver)
        channelToReceiverThreadList.append(t)
        for i in range(no_senders):
            s = threading.Thread(name='SignalThread' + str(sender + 1), target=self.send_busy_signal(sender))
            channelToSenderThreadList.append(s)
            sender=sender+1

        for thread in channelToReceiverThreadList:
            thread.start()

        for thread in channelToSenderThreadList:
            thread.start()

        for thread in channelToReceiverThreadList:
            thread.join()

        for thread in channelToSenderThreadList:
            thread.join()



