import threading
import multiprocessing
import channel_csma
import sender_csma
import receiver_csma
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


def start():
    # writeFromSenderToChannel = []
    # readFromSenderToChannel = []

    writeFromChannelToSender = []
    readFromChannelToSender = []

    writeFromChannelToReceiver = []
    readFromChannelToReceiver = []

    writeFromReceiverToChannel = []
    readFromReceiverToChannel = []

    for i in range(no_senders):
        readHead, writeHead = multiprocessing.Pipe()
        writeFromChannelToSender.append(writeHead)
        readFromChannelToSender.append(readHead)

    for i in range(no_senders):
        readHead, writeHead = multiprocessing.Pipe()
        writeFromChannelToReceiver.append(writeHead)
        readFromChannelToReceiver.append(readHead)

    readFromSenderToChannel, writeFromSenderToChannel = multiprocessing.Pipe()

    senderList = []
    receiverList = []

    print('1. 1-persistent method')
    print('2. Non-persistent method')
    print('3. p-persistent method')
    ch=int(input('Enter your choice(1-3):'))

    for i in range(no_senders):
        sender = sender_csma.Sender(i,'input' + str(i) + '.txt',writeFromSenderToChannel,readFromChannelToSender[i],ch)
        senderList.append(sender)

    for i in range(no_receivers):
        receiver = receiver_csma.Receiver(i,readFromChannelToReceiver[i])
        receiverList.append(receiver)

    channel = channel_csma.Channel(readFromSenderToChannel,writeFromChannelToSender,readFromReceiverToChannel,writeFromChannelToReceiver)

    senderThreads = []
    receiverThreads = []

    for i in range(len(senderList)):
        p = threading.Thread(target=senderList[i].transmit)
        senderThreads.append(p)

    for i in range(len(receiverList)):
        p = threading.Thread(target=receiverList[i].startReceiving)
        receiverThreads.append(p)

    channelThread = threading.Thread(target=channel.start_channel)

    channelThread.start()

    for thread in receiverThreads:
        thread.start()

    for thread in senderThreads:
        thread.start()

    for thread in senderThreads:
        thread.join()

    channelThread.join()

    for thread in receiverThreads:
        thread.join()


if __name__ == "__main__":
    start()