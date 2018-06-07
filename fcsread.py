# test read fcs files
import os
import struct
import numpy as np 

def readHeader(filedir):
    x = open(filedir,'rb')
    header_text = read_header(x)[0]
    header =  read_header(x)[1]
    headerdic = header_text_read(header_text)
    dickeys = str(headerdic)
    bit = []
    datarange = []
    name = []
    name2 = []
    for i in range(1,int(headerdic['PAR'])+1 ):
        if dickeys.find('P%dS'%i) == -1:
            headerdic['P%dS'%i] = headerdic['P%dN'%i]
    for i in range(1,int(headerdic['PAR'])+1 ):
        bit.append(headerdic['P%dB' % i ])
        datarange.append(headerdic['P%dR' % i ])
        name.append(headerdic['P%dN' % i ])
        name2.append(headerdic['P%dS' % i ])
    data = read_bytes(x,header['data_start'],header['data_end'])
    fdata = struct.unpack('%s%d%s' % ('>', int(headerdic['TOT'])*int(headerdic['PAR']), 'f') ,data)

    dataarray = np.array(fdata).reshape((int(headerdic['TOT']),int(headerdic['PAR'])))
    headerTable = {}
    headerTable['headerDic'] = headerdic
    headerTable['bit'] = bit
    headerTable['dataRange'] = datarange
    headerTable['name'] = name
    headerTable['name2'] = name2
    headerTable['fileName'] = os.path.split(filedir)[1]

    return (dataarray,headerTable)

def read_bytes(self,start,stop):
    self.seek(start)
    return self.read(stop - start +1)

def read_header(self):
     
    header = {}
    header['version'] = float(read_bytes(self,3,5))
    header['text_start'] = int(read_bytes(self, 10, 17))
    header['text_stop'] = int(read_bytes(self, 18, 25))
    header['data_start'] = int(read_bytes(self, 26, 33))
    header['data_end'] = int(read_bytes(self, 34, 41))

    header_text = read_bytes(self,header['text_start'],header['text_stop'])

    return (header_text,header)

def header_text_read(header_text):
    header_str = str(header_text)
    separator = chr(header_text[1])
    spliter = header_str[2]
    header_list = header_str.split(separator)
    header_out = {}
    if spliter == '\\':
        spliter = '\\\\'

    for i in header_list:
        header_value = i.split(spliter)
        header_out[header_value[0]] = header_value[1]
    return header_out



