import termios
import serial
from collections import deque

# declared in octal  
GARBAGE_CHAR = 0123
SLIP_END = 0300
SLIP_ESC = 0333
SLIP_ESC_END = 0334
SLIP_ESC_ESC = 0335
DEBUG_MAKER = 0015
MAX_MTU = 200
readBufferQueue = deque([])

# This function takes a byte list, encode it in SLIP protocol and return the encoded byte list  
def encodeToSLIP(byteList):
    tempSLIPBuffer = []
    tempSLIPBuffer.append(SLIP_END)

    # UGLY HACK
    # Append garbage characters to avoid a bug where the 2nd and 3rd byte
    # are not interpreted by the MCU
    # tempSLIPBuffer.append(GARBAGE_CHAR)
    # tempSLIPBuffer.append(GARBAGE_CHAR)

    # print(byteList + '\n')
    for i in byteList:
        if i == SLIP_END:
            tempSLIPBuffer.append(SLIP_ESC)
            tempSLIPBuffer.append(SLIP_ESC_END)
        elif i == SLIP_ESC:
            tempSLIPBuffer.append(SLIP_ESC)
            tempSLIPBuffer.append(SLIP_ESC_ESC)
        else:
            tempSLIPBuffer.append(i)
    tempSLIPBuffer.append(SLIP_END)
    return tempSLIPBuffer

# This function uses getSerialByte() function to get SLIP encoded bytes from the serial port and return a decoded byte list  
def decodeFromSLIP(serialFD):
    dataBuffer = []
    while 1:
        # serialByte = getSerialByte(serialFD)
        # serialByte = ord(serialFD.read())
        serialByte = serialFD.read()
        intSerialByte = ord(serialByte)
        # print("Got a serial byte: " + str(serialByte))
        if intSerialByte is None:
            return -1
        elif intSerialByte == SLIP_END:
            if len(dataBuffer) > 0:
                # print(dataBuffer)
                # print('len of data_buffer is ' + str(len(dataBuffer)))
                # for x in xrange(0,len(dataBuffer)-1):
                    # if type(dataBuffer[x]) == int:
                        # print('dataBuffer['+str(x)+'] = '+ str(dataBuffer[x]))
                return ''.join(dataBuffer)
        elif intSerialByte == SLIP_ESC:
            # serialByte = getSerialByte(serialFD)
            serialByte = serialFD.read()
            intSerialByte = ord(serialByte)
            # serialByte = ord(serialFD.read())
            if intSerialByte is None:
                return -1 
            elif intSerialByte == SLIP_ESC_END:
                dataBuffer.append('\xc0')
            elif intSerialByte == SLIP_ESC_ESC:
                dataBuffer.append('\xdb')
            # elif intSerialByte == DEBUG_MAKER:
            #     dataBuffer.append(DEBUG_MAKER)
            else:
                print("Protocol Error")
        else:
             dataBuffer.append(serialByte)
    return -1

# This function read byte chuncks from the serial port and return one byte at a time  
def getSerialByte(serialFD):
    if len(readBufferQueue) == 0:
        #fetch a new data chunk from the serial port       
        i = 0
        while len(readBufferQueue) < MAX_MTU:
            newByte = ord(serialFD.read())
            readBufferQueue.append(newByte)
        newByte = readBufferQueue.popleft()
        return newByte
    else:
        newByte = readBufferQueue.popleft()
        return newByte
