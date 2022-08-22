import string


def vrc(data,parity='odd'):    # returns codeword according to VRC
    n=0
    for ch in data:
        if ch == '1':
            n=n+1
    if n%2 ==0 and parity=='odd':    # even number of 1's
        codeword=data+'1'
    elif parity=='odd':
        codeword=data+'0'
    elif n%2==0:
        codeword=data+'0'
    else:
        codeword=data+'1'
    return codeword


def detect_error_vrc(codeword,parity='odd'):    # returns true if error is detected, false if there is no error
    n = 0
    for ch in codeword:
        if ch == '1':
            n = n + 1
    if n%2==0 and parity=='odd':
        return True
    elif parity=='odd':
        return False
    elif n%2==0:
        return False
    else:
        return True


def lrc(data,parity='odd'):   # returns codeword according to LRC
    codeword=data
    n=[0,0,0,0]
    i=0
    for ch in data:
        if ch=='1':
            n[i%4]=n[i%4]+1
        i=i+1
    if parity=='odd':
        for x in n:
            if x%2==0:
                codeword=codeword+'1'
            else:
                codeword=codeword+'0'
    else:
        for x in n:
            if x%2==0:
                codeword=codeword+'0'
            else:
                codeword=codeword+'1'
    return codeword


def detect_error_lrc(codeword,parity='odd'):   # returns True if error is detected, otherwise False
    n=[0,0,0,0]
    i=0
    for ch in codeword:
        if ch=='1':
            n[i%4]=n[i%4]+1
        i=i+1
    if parity=='odd':
        for x in n:
            if x%2==0:
                return True
        return False
    else:
        for x in n:
            if x%2==1:
                return True
        return False


def checksum(data):   # returns codeword according to checksum scheme
    codeword=data
    s=0
    i=0
    while i<len(data):
        s=s+int(data[i:i+4],2)
        i=i+4
    sum=bin(s)[2:]
    while len(sum)!=4:
        if len(sum)<4:  # no carry and beginning digits are 0's
            sum='0'*(4-len(sum))+sum
        elif len(sum)>4:  # if there is carry
            sum=bin(int(sum[(len(sum)-4):],2)+int(sum[0:(len(sum)-4)],2))[2:]
    for x in sum:   # complementing the sum
        if x=='0':
            codeword+='1'
        else:
            codeword+='0'
    return codeword


def detect_error_checksum(codeword):  # returns True if error is detected, otherwise returns False
    s=0
    i=0
    while i<len(codeword):
        s=s+int(codeword[i:i+4],2)
        i=i+4
    sum=bin(s)[2:]
    while len(sum)!=4:
        if len(sum)<4:  # no carry and beginning digits are 0's
            sum='0'*(4-len(sum))+sum
        elif len(sum)>4:   # if there is carry
            sum=bin(int(sum[(len(sum)-4):],2)+int(sum[0:(len(sum)-4)],2))[2:]
    for x in sum:
        if x=='0':   # on complementing, it will become a 1, so result is non-zero
            return True    # error detected
    return False


def crc(data,poly='111010101'):   # crc-8 default polynomial
    codeword=data
    data+='0'*(len(poly)-1)
    a=data[0:len(poly)]
    rem=''
    i=len(poly)
    while True:
        rem=bin(int(a,2)^int(poly,2))[2:]
        if (i+(len(poly)-len(rem)))>len(data):
            a=rem+data[i:]
            break
        a=rem+data[i:i+(len(poly)-len(rem))]
        i=i+(len(poly)-len(rem))
    if len(a)<(len(poly)-1):
        a='0'*(len(poly)-len(a)-1)+a
    codeword+=a
    return codeword


def detect_error_crc(codeword,poly='111010101'):   # crc-8 default polynomial
    a=codeword[0:len(poly)]
    i=len(poly)
    while True:
        rem = bin(int(a, 2) ^ int(poly, 2))[2:]
        if (i + (len(poly) - len(rem))) > len(codeword):
            a = rem + codeword[i:]
            break
        a = rem + codeword[i:i + (len(poly) - len(rem))]
        i = i + (len(poly) - len(rem))
    if int(a,2)==0:
        return False
    else:
        return True


if __name__=='__main__':
    #codeword=input('Enter the codeword to be checked:')
    #p=input('Enter the crc polynomial:')
    print(crc('0000000000000000','10001001'))
    print(vrc('0000000000000000'))
    if detect_error_vrc('00000000100010011'):
        print('Error detected by VRC')
    else:
        print('No error detected by VRC')
    '''if detect_error_lrc('10001010111000110010'):
        print('Error detected by LRC')
    else:
        print('No error detected by LRC')
    if detect_error_checksum('00000011101010101011'):
        print('Error detected by Checksum')
    else:
        print('No error detected by Checksum')'''
    if detect_error_crc('0000000010001001','10001001'):
        print('Error detected by CRC')
    else:
        print('No error detected by CRC')
