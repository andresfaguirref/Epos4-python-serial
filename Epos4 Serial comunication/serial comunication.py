
import serial, time
import crc16

def crc16(string_data_hex):
    import crc16
    try:
        ascii_data = string_data_hex.decode("hex") 
        dec_crc = crc16.crc16xmodem(ascii_data)
        hex_crc = hex(dec_crc)
        return hex_crc,dec_crc,ascii_data
    except:
        print('The input data is not valid')
        return


ser = serial.Serial()
#ser.port = "/dev/ttyUSB0"
ser.port = "COM23"
#ser.port = "/dev/ttyS2"
ser.baudrate = 115200
ser.bytesize = serial.EIGHTBITS #number of bits per bytes
ser.parity = serial.PARITY_NONE #set parity check: no parity
ser.stopbits = serial.STOPBITS_ONE #number of stop bits
#ser.timeout = None          #block read
ser.timeout = 1            #non-block read
#ser.timeout = 2              #timeout block read
ser.xonxoff = False     #disable software flow control
ser.rtscts = False     #disable hardware (RTS/CTS) flow control
ser.dsrdtr = False       #disable hardware (DSR/DTR) flow control
ser.writeTimeout = 2     #timeout for write

try: 
    ser.open()
except Exception, e:
    print "error open serial port: " + str(e)
    exit()

if ser.isOpen():

    w=1

    try:
        ser.flushInput() #flush input buffer, discarding all its contents
        ser.flushOutput()#flush output buffer, aborting current output 
                 #and discard all that is in buffer

        t = 0
        ascii_data = ''
        if w == 0:
        
            # DLE (0x90)
            mesL = "\x90"
            ser.write(mesL)
            print("write data: %s" % (mesL))
            #time.sleep(t)
            

            # STX (0x02)
            mesH = "\x02"
            ser.write(mesH)
            print("write data: %s" % (mesH))
            #time.sleep(t)

            # OpCode (0x60,0x68)
            mesL = "\x60"
            ser.write(mesL)
            print("write data: %s" % (mesL))
            
            #time.sleep(t)

            # Len
            mesH = "\x02"
            ser.write(mesH)
            print("write data: %s" % (mesH))
            ascii_data = mesH + mesL
            #time.sleep(t)

            # LowByte Data[0] (Node ID)
            mesL = "\x01"
            ser.write(mesL)
            print("write data: %s" % (mesL))
            #time.sleep(t)

            # HighByte Data[0] (LowByte Index)
            mesH = "\x64"
            ser.write(mesH)
            print("write data: %s" % (mesH))
            ascii_data = ascii_data + mesH + mesL
            #time.sleep(t)

            # LowByte Data[1] (HighByte Index)
            mesL = "\x60"
            ser.write(mesL)
            print("write data: %s" % (mesL))
            #time.sleep(t)

            # HighByte Data[1] (Subindex)
            mesH = "\x00"
            ser.write(mesH)
            print("write data: %s" % (mesH))
            ascii_data = ascii_data + mesH + mesL
            #time.sleep(t)

            import crc16
            dec_crc = crc16.crc16xmodem(ascii_data)
            hex_crc = hex(dec_crc)

            mesH = hex_crc[2] + hex_crc[3]
            mesL = hex_crc[4] + hex_crc[5]

            mesH = mesH.decode("hex")
            mesL = mesL.decode("hex")
            
            # CRC LowByte
            #mesL = "\x29"
            ser.write(mesL)
            print("write data: %s" % (mesL))
            #time.sleep(t)

            # CRC HighByte
            #mesH = "\x5a"
            ser.write(mesH)
            print("write data: %s" % (mesH))
            #time.sleep(t)

        else:
            
            # DLE (0x90)
            mesL = "\x90"
            ser.write(mesL)
            print("write data: %s" % (mesL))
            #time.sleep(t)

            # STX (0x02)
            mesH = "\x02"
            ser.write(mesH)
            print("write data: %s" % (mesH))
            #time.sleep(t)

            # OpCode 
            mesL = "\x68"
            ser.write(mesL)
            print("write data: %s" % (mesL))
            #time.sleep(t)

            # Len 
            mesH = "\x04"
            ser.write(mesH)
            print("write data: %s" % (mesH))
            ascii_data = mesH + mesL
            #time.sleep(t)

            # LowByte Data[0] (Node ID) (W0 L0)
            mesL = "\x01"
            ser.write(mesL)
            print("write data: %s" % (mesL))
            #time.sleep(t)

            # HighByte Data[0] (WORD) (Low Byte Index of Object) (W0 H0)
            mesH = "\x40"
            ser.write(mesH)
            print("write data: %s" % (mesH))
            ascii_data = ascii_data + mesH + mesL
            #time.sleep(t)

            # LowByte Data[1] (WORD) (High part Index of Object) (W1 L1)
            mesL = "\x60"
            ser.write(mesL)
            print("write data: %s" % (mesL))
            #time.sleep(t)

            # HighByte Data[1] (Subindex) (W1 H1)
            mesH = "\x00"
            ser.write(mesH)
            print("write data: %s" % (mesH))
            ascii_data = ascii_data + mesH + mesL
            #time.sleep(t)

            # LowByte Data[2] (D0) (W2 L2)
            mesL = "\x00"
            ser.write(mesL)
            print("write data: %s" % (mesL))
            #time.sleep(t)

            # HighByte Data[2] (D1) (W2 H2)
            mesH = "\x00"
            ser.write(mesH)
            print("write data: %s" % (mesH))
            ascii_data = ascii_data + mesH + mesL
            #time.sleep(t)

            # LowByte Data[3] (D2) (W3 L3)
            mesL = "\x00"
            ser.write(mesL)
            print("write data: %s" % (mesL))
            #time.sleep(t)

            # HighByte Data[3] (D3) (W3 H3)
            mesH = "\x00"
            ser.write(mesH)
            print("write data: %s" % (mesH))
            ascii_data = ascii_data + mesH + mesL
            #time.sleep(t)

            import crc16
            dec_crc = crc16.crc16xmodem(ascii_data)
            hex_crc = hex(dec_crc)
            if len(hex_crc) < 6:
               while len(hex_crc) < 6:
                   hex_crc = hex_crc[:2] + '0' + hex_crc[2:]

            print(hex_crc)
            mesH = hex_crc[2] + hex_crc[3]
            mesL = hex_crc[4] + hex_crc[5]

            mesH = mesH.decode("hex")
            mesL = mesL.decode("hex")

            # CRC LowByte
            #mes = "\x01"
            ser.write(mesL)
            print("write data: %s" % (mesL))
            #time.sleep(t)

            # CRC HighByte
            #mes = "\xe8"
            ser.write(mesH)
            print("write data: %s" % (mesH))
            #time.sleep(t)
        

        numOfLines = 0
        vec = []
        while True:
            response = ser.readline()
            vec.append(response)
            #print("read data: " + response)

            numOfLines = numOfLines + 1

            if (numOfLines >= 1):
                break

        ser.close()
        print(vec)
        
    except Exception, e1:
        print "error communicating...: " + str(e1)

else:
    print "cannot open serial port "
