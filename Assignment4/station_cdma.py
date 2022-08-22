import time


class Station:
    def __init__(self,num,walsh):
        self.n=num
        self.wc=walsh
        self.ptr=0
        self.fc=''

    def set_file_name(self,file):
        f=open(file,'r')
        self.fc=f.read()
        f.close()
        self.ptr=0

    def bit_to_send(self):
        if self.ptr<len(self.fc):
            ch=self.fc[self.ptr]
            self.ptr=self.ptr+1
            if ch=='0':
                return -1
            else:
                return 1
        else:
            return 0

    def send_to_channel(self):
        bit=self.bit_to_send()
        encoded_data=[0 for _ in range(len(self.wc))]
        for i in range(len(self.wc)):
            encoded_data[i]=(bit*(self.wc[i]))
        return encoded_data

    def reconstruct_data(self,composite_data,walsh_st):
        i=0
        sum=0
        while i< len(composite_data):
            sum=sum+(composite_data[i]*walsh_st[i])
            time.sleep(0.002)
            i=i+1
        # print(sum)
        b=sum/self.n
        # print(b)
        if b==0:
            print('Station having walsh code ',walsh_st,' is silent')
        elif b==-1:
            print('Station having walsh code ',walsh_st,' sent bit 0')
        elif b==1:
            print('Station having walsh code ', walsh_st, ' sent bit 1')


if __name__=='__main__':
    s=Station(4,[-1,-1,-1,-1])
    s.set_file_name('Send1.txt')
    # print(s.send_to_channel())
    # print(s.send_to_channel())
    s.reconstruct_data([-1,-1,-3,1],[1,-1,1,-1])
