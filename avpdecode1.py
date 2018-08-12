#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Time: 2018/7/30 21:59
# Version: 0.1
# __author__: Jie Cheng D <jie.d.cheng@outlook.com>

import struct
from avpAttr import avpAttr
from avpRaw import MAR,UDR,UDA

# UDR88 = '0100013cc0000132010000011416f6191416f61900000\
# 107400000386a70796f6d74617330312e696d736e772e6b6464692e6e\
# 652e6a703b31333734343530383b333933343930303736343b0000012\
# 840000018696d736e772e6b6464692e6e652e6a700000010840000023\
# 6a70796f6d74617330312e696d736e772e6b6464692e6e652e6a70000\
# 0000104400000200000010a4000000c000028af000001024000000c01\
# 000001000001154000000c000000010000011b40000018696d736e772\
# e6b6464692e6e652e6a7000000125400000226a70796f74656b30312e\
# 696d736e772e6b6464692e6e652e6a700000000002bcc000003c00002\
# 8af00000259c000002e000028af7369703a2b38313830383838363030\
# 303040696d736e772e6b6464692e6e652e6a700000000002bfc000001\
# 0000028af00000011'


UDR = bytes.fromhex(UDR)
MAR0 = bytes.fromhex(MAR)
UDA0 = bytes.fromhex(UDA)
# print(MAR0)

class AvpDecode:


    def __init__(self, avpBytes):
        self.version = '0x01'
        self.__diaLength = int.from_bytes(avpBytes[1:4], 'big')
        self.__diaFlags = hex(avpBytes[4])
        self.__cmdCode = int.from_bytes(avpBytes[5:8], 'big')
        self.__applicationID = int.from_bytes(avpBytes[8:12], 'big')
        self.__hopByHopIden = hex(int.from_bytes(avpBytes[12:16], 'big'))
        self.__end2EndIden = hex(int.from_bytes(avpBytes[16:20], 'big'))
        self.__avpStart = avpBytes[20:]


    @classmethod
    def diamFlags(cls, flagCode):
        diaFlags = ["Request", "Proxyable", "Error", "T"]
        binFlags = bin(int(flagCode[2:], 16))
        flags = []
        for i in range(2,6):
            if binFlags[i] == '1':
                flags.append(diaFlags[i-2])
        return ','.join(flags)


    @classmethod
    def avpDecoding(cls, avpStream):

        code = int.from_bytes(avpStream[:4],'big')
        attr = avpAttr.get(str(code))
        flags = hex(int(attr[2]))
        length = int.from_bytes(avpStream[5:8], 'big')
        rem = length%4
        if rem in (1,2,3):
            move = length + 4 - rem
        else:
            move = length
        if flags not in ("0xc0","0x80","0xe0"):
            if attr[1] in ("Integer32","Unsigned32","Integer64","Unsigned64"):
                val = int.from_bytes(avpStream[8:length], 'big')
                print(f"AVP: {code} l={length} f={flags} val={val}")
            elif attr[1] == "OctetString":
                val = avpStream[8:length]
                print(f"AVP: {code} l={length} f={flags} val={val}")
            elif attr[1] == "Grouped":
                print(f"AVP: {code} l={length} f={flags} val...")
                AvpDecode.avpDecoding(avpStream[8:length+8])
        else:
            vendorID = '3GPP (10415)'
            if attr[1] in ("Integer32","Unsigned32","Integer64","Unsigned64"):
                val = int.from_bytes(avpStream[12:length], 'big')
                print(f"AVP: {code} l={length} f={flags} vnd={vendorID} val={val}")
            elif attr[1] == "OctetString":
                val = avpStream[12:length]
                print(f"AVP: {code} l={length} f={flags} vnd={vendorID} val={val}")
            elif attr[1] == "Grouped":
                print(f"AVP: {code} l={length} f={flags} vnd={vendorID} val...")
                AvpDecode.avpDecoding(avpStream[12:length+8])

        if len(avpStream[move:]) > 12:
            AvpDecode.avpDecoding(avpStream[move:])
        else:
            return

    def decodeavp(self):
        print("Diameter Protocal")
        print(f' Version: {self.version}')
        print(f' Length: {self.__diaLength}')
        print(f' Flags: {self.__diaFlags} {AvpDecode.diamFlags(self.__diaFlags)}')
        print(f' Command Code: {self.__cmdCode}')
        print(f' ApplicationID: {self.__applicationID}')
        print(f' Hop-by-Hop Identifier: {self.__hopByHopIden}')
        print(f' End-to-End Identifier: {self.__end2EndIden}')
        AvpDecode.avpDecoding(self.__avpStart)



if __name__ == "__main__":

    udr = AvpDecode(UDR)
    udr.decodeavp()
    mar = AvpDecode(MAR0)
    mar.decodeavp()
    uda = AvpDecode(UDA0)
    uda.decodeavp()



