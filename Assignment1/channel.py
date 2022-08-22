from random import random


def inject_random_error(data):   # flips bits at random
    errdata = ''
    for i in range(len(data)):
        x = int(random() * 2)
        if x == 1:  # flip the bit
            if data[i] == '0':
                errdata += '1'
            else:
                errdata += '0'
        else:
            errdata += data[i]
    return errdata


def inject_single_bit_error(data):   # injects single-bit error
    x = int(random()*(2*len(data)))
    if x<len(data):
        if data[x]=='0':
            data=data[0:x]+'1'+data[(x+1):]
        else:
            data=data[0:x]+'0'+data[(x+1):]
    return data


def inject_burst_error(data, l):   # injects burst error of length l
    x = int(random()*2*(len(data) - l))
    if x<(len(data)-l):
        if data[x]=='0':
            errdata=data[0:x]+'1'
        else:
            errdata=data[0:x]+'0'
        i=1
        while i<(l-1):
            y = int(random() * 2)
            if y == 1:  # flip the bit
                if data[x+i] == '0':
                    errdata += '1'
                else:
                    errdata += '0'
            else:
                errdata +=data[x+i]
            i+=1
        if data[x+l-1]=='0':
            errdata+='1'
        else:
            errdata+='0'
        errdata+=data[(x+l):]
    else:
        errdata=data
    return errdata


def inject_error(data):   # injects error to the dataword by calling the appropriate function
    x=int(random()*3)
    # print('Press 1 for single-bit error, 2 for burst error, 3 for random errors')
    # x=int(input('Enter your choice:'))
    # x=2
    if x==0:
        data=inject_single_bit_error(data)
    elif x==1:
        data=inject_burst_error(data,int(random()*len(data)/2)+2)
    elif x==2:
        data=inject_random_error(data)
    return data

