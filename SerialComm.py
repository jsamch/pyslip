import ProtoSLIP
import termios
import serial
import platform

# This function connect and configure the serial port. Then returns the file discripter  
def connectToSerialPort():
    if platform.system() == 'Windows':
        port = 'COM1'
    elif platform.system() == 'Linux':
        port = '/dev/ttyUSB0'
    else:
        print('Unrecognized platform')
        return

    serialFD = serial.Serial(port=port, baudrate=115200, bytesize=8, parity='N', stopbits=1, xonxoff=False, rtscts=False)
    # port='/dev/ttyUSB0'- port to open  
    # baudrate=500000  - baud rate to communicate with the port  
    # bytesize=8           - size of a byte  
    # parity='N'           - no parity  
    # stopbits=1           - 1 stop bit  
    # xonxoff=False           - no software handshakes  
    # rtscts=False           - no hardware hand shakes  
    if serialFD < 0:
        print("Couldn't open serial port")
        return -1
    else:
        # print("Opened serial port")
        return serialFD

# This function accept a byte array and write it to the serial port  
def writeToSerialPort(serialFD, byteArray):
    encodedSLIPBytes = ProtoSLIP.encodeToSLIP(byteArray)
    #convert byte list to a string
    byteString = ''.join(chr(b) for b in encodedSLIPBytes)
    # print(byteString)
    # print ('\nWriting ' + str(byteString)) 
    serialFD.write(byteString)
    return


# This function reads from the serial port and return a byte array  
def readFromSerialPort(serialFD):
    i = 1
    byteArray = None
    byteArray = ProtoSLIP.decodeFromSLIP(serialFD)
    if byteArray is None:
        print "readFromSerialPort(serialFD): Error"
        return -1
    else:
        return byteArray

# This function reads from the serial port and return a byte array  
def disconnectFromSerialPort(serialFD):
    serialFD.close()
    return

if __name__ == '__main__':
    connectToSerialPort()