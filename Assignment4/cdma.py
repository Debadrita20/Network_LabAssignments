import walshcode
import time
import channel_cdma
import station_cdma

if __name__=="__main__":
    n=int(input("Enter the number of stations: "))
    p=walshcode.getpof2(n)
    w=[[0 for i in range(p)] for j in range(p)]
    walshcode.buildWalshTable(w,p,0,p-1,0,p-1)
    # print(w)
    stations_list=[]
    cpt=0
    trt=0
    for i in range(n):
        st=station_cdma.Station(n,w[i])
        st.set_file_name('cdmafile'+str(1+(i%4))+'.txt')
        stations_list.append(st)
    ch=channel_cdma.Channel(n)
    for i in range(20):  # 20 time slots tested
        ch.refresh_channel()  # so that the channel contains 0's at the beginning of each time slot
        st_time=time.time()
        for st in stations_list:
            d=st.send_to_channel()
            # print('Station ',(stations_list.index(st)+1),' sends ',d)
            time.sleep(0.005)
            ch.receive_data_from_station(d)
        cpt+=(time.time()-st_time)
        print('Data in channel now: ',ch.get_channel_data())
        print('Data from station 1 is to be reconstructed')
        stations_list[n-1].reconstruct_data(ch.get_channel_data(),w[0])
        trt+=(time.time()-st_time)
        print('------------next time slot-----------------')
    print('Total channel processing time:',cpt,' s')
    print('Total transmission time:',trt,' s')

