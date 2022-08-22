import errordetect


#  preamble + sfd + dest + source + seqNo +len/type + data + crc
#     7     +  1  +  6   +   6    +  1    +  1 +  46  +   4  =  72

def make_packet(seqNo,data,sender,destination,type=-1):
    preamble = '01' * 28
    sfd = '10101011'
    sequence_bits = '{0:08b}'.format(int(seqNo))
    destination_address = '{0:048b}'.format(int(destination))
    if type==-1:
        length = '{0:008b}'.format(len(data))
    else:
        length= '{0:008b}'.format(type)
    source_address = '{0:048b}'.format(int(sender))
    if len(data)<(46*8):
        data=data+'0'*(46*8-len(data))
    pkt = preamble + sfd + destination_address + source_address + sequence_bits + length + data
    pkt = errordetect.crc(pkt,'100000100110000010001110110110111')
    return pkt


def extract_data(p):
    data = p[176:544]
    l=int(p[168:176],2)
    return data[0:l]    # gets rid of the padding


def get_dest_address(p):
    d = p[64:112]
    return int(d,2)


def get_src_address(p):
    s = p[112:160]
    return int(s,2)


def is_error_free(p):
    if errordetect.detect_error_crc(p,'100000100110000010001110110110111'):
        return False
    else:
        return True


def get_seq_no(p):
    sno = p[160:168]
    return int(sno, 2)


def get_type(p):
    t=p[168:176]
    return int(t,2)
