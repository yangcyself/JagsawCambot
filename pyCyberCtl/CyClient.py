# -^- coding: utf-8 -^-
import socket
import sys
import struct
import numpy as np
import cv2
import matplotlib.pyplot as plt

BufferSize = 30000
PORT = 19876
def convertEndine(inputbytes, n = 8):
    outputbytes=bytearray()
    for i in range(0,len(inputbytes),n):
        tmp = inputbytes[i:i+n] 
        outputbytes += tmp[::-1]
    return outputbytes

class Client:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server_address = ('localhost', PORT)
    def sayHello(self):
        message = "hello"
        sent = self.sock.sendto(message.encode(), self.server_address)
        data, server = self.sock.recvfrom(4096)
        print("received: ",data.decode())
    def getPic(self):
        message = 'GET'
        sent = self.sock.sendto(message.encode(), self.server_address)

        # Receive response
        data, server = self.sock.recvfrom(65532)
        print("received: ")
        x,y,c = struct.unpack('iii', convertEndine(data[:12],4)) 
        total = x*y*c - BufferSize
        print(x,y,c)
        data = data[12:]
        print(len(data))
        while(total>0):
            total -= BufferSize
            d, server = self.sock.recvfrom(40960)
            data+=d
        file_bytes  = np.frombuffer(bytearray(data), dtype=np.uint8)
        file_bytes = file_bytes.reshape((x,y,c))
        return file_bytes
    def getPos(self):
        message = 'GetPos'
        sent = self.sock.sendto(message.encode(), self.server_address)

        # Receive response
        data, server = self.sock.recvfrom(4096)
        print("received: ")
        #convert Endine
#         res = struct.unpack('ii', convertDoubleEndine(data[:-1])) 
        # print(len(data))
        res = struct.unpack('dd', convertEndine(data[:-1],8)) 
        res = (*res, data[-1])
        print(res)
        return res
    
    def takAction(self,action,x,y):
        # action : 0: move relative 1: move definative 2: taponce 3: tapdown 4: tapup
        MessageHead = 'Maaa'# 是有补位的！！！
        bytesArray = MessageHead.encode() 
        var = struct.pack('iii',action,x,y) 
#         var = convertEndine(var,4)
        bytesArray+= var
        # Send data
        sent = self.sock.sendto(bytesArray, self.server_address)
        data, server = self.sock.recvfrom(4096)
        print("received: ",data.decode())
        
    def __del__(self):
        self.sock.close()

