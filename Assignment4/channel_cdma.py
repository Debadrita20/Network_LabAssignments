import time
import walshcode


class Channel:
    def __init__(self,n):
        self.n=n
        x=walshcode.getpof2(self.n)
        self.data=[0 for _ in range(x)]

    def refresh_channel(self):
        for i in range(len(self.data)):
            self.data[i]=0;

    def get_channel_data(self):
        return self.data

    def receive_data_from_station(self,d):
        for i in range(len(self.data)):
            self.data[i]+=d[i]
            time.sleep(0.002)


if __name__=='__main__':
    ch=Channel(4)
    print(ch.get_channel_data())
    ch.receive_data_from_station([-1,-1,-1,-1])
    print(ch.get_channel_data())
    ch.receive_data_from_station([-1,1,-1,1])
    ch.receive_data_from_station([0,0,0,0])
    ch.receive_data_from_station([1,-1,-1,1])
    print(ch.get_channel_data())



