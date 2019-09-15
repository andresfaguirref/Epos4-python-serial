import serial, time
import crc16

class SerialEpos4(object):
    def __init__(self,Port,NodeID):
        
        #Serial Configuration
        self.serial = serial.Serial()
        self.serial.port = Port
        self.serial.baudrate = 115200
        self.serial.bytesize = serial.EIGHTBITS
        self.serial.parity = serial.PARITY_NONE
        self.serial.stopbits = serial.STOPBITS_ONE
        self.serial.timeout = 1
        self.serial.xonxoff = False     
        self.serial.rtscts = False     
        self.serial.dsrdtr = False       
        self.serial.writeTimeout = 2

        #Node ID CAN configuration
        self.NodeID = NodeID  
    
    def OpenPort(self):
        try: 
            self.serial.open()
            self.serial.flushInput() #flush input buffer, discarding all its contents
            self.serial.flushOutput()#flush output buffer, aborting current output 
                 #and discard all that is in buffer
        except Exception, e:
            print "error open serial port: " + str(e)
            exit()

    def ClosePort(self):
        try: 
            self.serial.close()
        except Exception, e:
            print "error open serial port: " + str(e)
            exit()

    def ReadPort(self,N_lines):
        vec = []
        numOfLines = 0
        while True:
            response = self.serial.readline()
            vec.append(response)
            numOfLines = numOfLines + 1
            if (numOfLines >= N_lines):
                break
        return vec

    def crc16_est(self,data_in_ascii):
        import crc16
        dec_crc = crc16.crc16xmodem(data_in_ascii)
        hex_crc = hex(dec_crc)
        if len(hex_crc) < 6:
            while len(hex_crc) < 6:
                hex_crc = hex_crc[:2] + '0' + hex_crc[2:]
        return hex_crc

    def hex_str_2_INT32(self,hex_str):
        if len(hex_str) == 8:
            Las_p = int(hex_str[0],16)
            if Las_p > 7:
                Las_p = Las_p - 8
                new_num = str(Las_p) + hex_str[1:len(hex_str)]
                INT32_num = int(new_num,16) - 2147483648
                return int(INT32_num)

            else:
                return int(hex_str,16)

        else:
            if len(hex_str) > 8:
                print ("The input value has more than 4 Bytes")
                return None
            else:
                try:
                    return int(hex_str,16)
                except Exception, e:
                    print "error open serial port: " + str(e)
                    return None

    def INT32_2_hex_str(self,INT_32,FULL_4_Bytes=False):
        if INT_32 >= 0:
            hex_string = hex(INT_32)
        else:
            hex_string = hex(0xfFFFFFFF - (abs(INT_32) -1))
        if FULL_4_Bytes:
            if len(hex_string) < 10:
                while len(hex_string) < 10:
                    hex_string = hex_string[:2] + '0' + hex_string[2:]
            return hex_string
        else:
            return hex_string
            
        
    def ReadObject(self,Index,SubIndex,Node_ID = None,Show=False):
        if Node_ID == None:
            Node_ID = self.NodeID

        try:
            IndexHB = Index[0] + Index[1]
            IndexLB = Index[2] + Index[3]
            SubIndexByte = SubIndex[0] + SubIndex[1]
        except Exception, e1:
            print ("Error data input: " + str(e1))
            return None

        if Show: print("Emited Data")
        if Show: print("")
        
        ascii_data = ''
        # DLE (0x90)
        mesL = "\x90"
        self.serial.write(mesL)
        if Show: print("DLE: %s" % hex(ord(mesL)))
            
        # STX (0x02)
        mesH = "\x02"
        self.serial.write(mesH)
        if Show: print("STX: %s" % hex(ord(mesH)))
 
        # OpCode (0x60,0x68)
        mesL = "\x60"
        self.serial.write(mesL)
        if Show: print("OpCode: %s" % hex(ord(mesL)))
            
        # Len
        mesH = "\x02"
        self.serial.write(mesH)
        if Show: print("Len: %s" % hex(ord(mesH)))
        ascii_data = mesH + mesL

        # LowByte Data[0] (Node ID)
        #mesL = "\x01"
        mesL = Node_ID
        self.serial.write(mesL)
        if Show: print("Node ID: %s" % hex(ord(mesL)))

        # HighByte Data[0] (LowByte Index)
        mesH = IndexLB.decode("hex")
        self.serial.write(mesH)
        if Show: print("LowByte Index: %s" % hex(ord(mesH)))
        ascii_data = ascii_data + mesH + mesL

        # LowByte Data[1] (HighByte Index)
        mesL = IndexHB.decode("hex")
        self.serial.write(mesL)
        if Show: print("HighByte Index: %s" % hex(ord(mesL)))

        # HighByte Data[1] (Subindex)
        mesH = SubIndexByte.decode("hex")
        self.serial.write(mesH)
        if Show: print("Subindex: %s" % hex(ord(mesH)))
        ascii_data = ascii_data + mesH + mesL
 
        hex_crc = self.crc16_est(ascii_data)
        mesH = hex_crc[2] + hex_crc[3]
        mesL = hex_crc[4] + hex_crc[5]
        mesH = mesH.decode("hex")
        mesL = mesL.decode("hex")
            
        # CRC LowByte
        self.serial.write(mesL)
        if Show: print("CRC LowByte: %s" % hex(ord(mesL)))

        # CRC HighByte
        self.serial.write(mesH)
        if Show: print("CRC HighByte: %s" % hex(ord(mesH)))
        if Show: print("")

        answer = self.ReadPort(1)
        data = []

        if Show: print("Received Data")
        if Show: print(answer)
        if Show: print("")
        if len(answer[0]) == 0:
            print("No data received")
            return None
        else:
            for x in range(0,len(answer[0])):
                data.append(answer[0][x])

        if len(data) == 14:
            if Show:
                print("DLE: %s" % hex(ord(data[0])))
                print("STX: %s" % hex(ord(data[1])))
                print("OpCode: %s" % hex(ord(data[2])))
                print("Len: %s" % hex(ord(data[3])))
                print("DWORD (Err Cod Def) (LW-LB): %s" % hex(ord(data[4])))
                print("DWORD (Err Cod Def) (LW-HB): %s" % hex(ord(data[5])))
                print("DWORD (Err Cod Def) (HW-LB): %s" % hex(ord(data[6])))
                print("DWORD (Err Cod Def) (HW-HB): %s" % hex(ord(data[7])))

                print("DATA (LW-LB): %s" % hex(ord(data[8])))
                print("DATA (LW-HB): %s" % hex(ord(data[9])))
                print("DATA (HW-LB): %s" % hex(ord(data[10])))
                print("DATA (HW-HB): %s" % hex(ord(data[11])))
                print("CRC Low Byte: %s" % hex(ord(data[12])))
                print("CRC High Byte: %s" % hex(ord(data[13])))

            if (data[4] == "\x00") and (data[5] == "\x00") and (data[6] == "\x00") and (data[7] == "\x00"):
                DATA_R_HB = data[11] + data[10]
                DATA_R_LB = data[9] + data[8]
                DATA = DATA_R_HB + DATA_R_LB
                decimal_value = DATA.encode("hex")
                decimal_value = self.hex_str_2_INT32(decimal_value)
                if Show: print ('Data of 0x' + Index + ' 0x' + SubIndex + ' (Dec): ' + str(decimal_value))
                if Show: print ('Data of 0x' + Index + ' 0x' + SubIndex + ' (Hex): ' + '0x' + DATA_R_HB.encode("hex") + ' 0x' + DATA_R_LB.encode("hex"))
                return data,decimal_value,DATA.encode("hex")
            else:
                ERROR_R_HB = data[7] + data[6]
                ERROR_R_LB = data[5] + data[4]
                print ('Error Detected (Hex): ' + '0x' + ERROR_R_HB.encode("hex") + ' 0x' + ERROR_R_LB.encode("hex") )
                return None
        else:
            print('Error No Len 14')
            for x in range(0,len(data)):
                if Show: print("Data(%s): %s" % (x,hex(ord(data[x]))))
            return None

    def WriteObject(self,Index,SubIndex,Write_Data,Node_ID = None,Show=False):
        if Node_ID == None:
            Node_ID = self.NodeID

        try:
            IndexHB = Index[0] + Index[1]
            IndexLB = Index[2] + Index[3]
            SubIndexByte = SubIndex[0] + SubIndex[1]
            Write_Data_HW_HB = Write_Data[0] + Write_Data[1]
            Write_Data_HW_LB = Write_Data[2] + Write_Data[3]
            Write_Data_LW_HB = Write_Data[4] + Write_Data[5]
            Write_Data_LW_LB = Write_Data[6] + Write_Data[7]
        except Exception, e1:
            print ("Error data input: " + str(e1))
            return None

        if Show: print("Emited Data")
        if Show: print("")
        
        ascii_data = ''
        # DLE (0x90)
        mesL = "\x90"
        self.serial.write(mesL)
        if Show: print("DLE: %s" % hex(ord(mesL)))
            
        # STX (0x02)
        mesH = "\x02"
        self.serial.write(mesH)
        if Show: print("STX: %s" % hex(ord(mesH)))
 
        # OpCode (0x60,0x68)
        mesL = "\x68"
        self.serial.write(mesL)
        if Show: print("OpCode: %s" % hex(ord(mesL)))
            
        # Len
        mesH = "\x04"
        self.serial.write(mesH)
        if Show: print("Len: %s" % hex(ord(mesH)))
        ascii_data = mesH + mesL

        # # LowByte Data[0] (Node ID) (W0 L0)
        #mesL = "\x01"
        mesL = Node_ID
        self.serial.write(mesL)
        if Show: print("Node ID: %s" % hex(ord(mesL)))

        # HighByte Data[0] (WORD) (Low Byte Index of Object) (W0 H0)
        mesH = IndexLB.decode("hex")
        self.serial.write(mesH)
        if Show: print("LowByte Index: %s" % hex(ord(mesH)))
        ascii_data = ascii_data + mesH + mesL

        # LowByte Data[1] (WORD) (High part Index of Object) (W1 L1)
        mesL = IndexHB.decode("hex")
        self.serial.write(mesL)
        if Show: print("HighByte Index: %s" % hex(ord(mesL)))

        # HighByte Data[1] (Subindex) (W1 H1)
        mesH = SubIndexByte.decode("hex")
        self.serial.write(mesH)
        if Show: print("Subindex: %s" % hex(ord(mesH)))
        ascii_data = ascii_data + mesH + mesL

        # LowByte Data[2] (D0) (W2 L2)
        mesL = Write_Data_LW_LB.decode("hex")
        self.serial.write(mesL)
        if Show: print("Data written (LW-LB) (D0): %s" % hex(ord(mesL)))

        # HighByte Data[2] (D1) (W2 H2)
        mesH = Write_Data_LW_HB.decode("hex")
        self.serial.write(mesH)
        if Show: print("Data written (LW-HB) (D1): %s" % hex(ord(mesH)))
        ascii_data = ascii_data + mesH + mesL

        # LowByte Data[3] (D2) (W3 L3)
        mesL = Write_Data_HW_LB.decode("hex")
        self.serial.write(mesL)
        if Show: print("Data written (HW-LB) (D2): %s" % hex(ord(mesL)))

        # HighByte Data[3] (D3) (W3 H3)
        mesH = Write_Data_HW_HB.decode("hex")
        self.serial.write(mesH)
        if Show: print("Data written (HW-HB) (D3): %s" % hex(ord(mesH)))
        ascii_data = ascii_data + mesH + mesL
 
        hex_crc = self.crc16_est(ascii_data)
        mesH = hex_crc[2] + hex_crc[3]
        mesL = hex_crc[4] + hex_crc[5]
        mesH = mesH.decode("hex")
        mesL = mesL.decode("hex")
            
        # CRC LowByte
        self.serial.write(mesL)
        if Show: print("CRC LowByte: %s" % hex(ord(mesL)))

        # CRC HighByte
        self.serial.write(mesH)
        if Show: print("CRC HighByte: %s" % hex(ord(mesH)))
        if Show: print("")

        answer = self.ReadPort(1)
        #data = []
        #if Show: print(answer)

    def Enable_to_move(self,Node_ID = None,Show = False):
        if Node_ID == None:
            Node_ID = self.NodeID
        self.WriteObject('6040','00','00000000',Node_ID,Show)
        time.sleep(0.1)
        self.WriteObject('6040','00','00000006',Node_ID,Show)
        time.sleep(0.1)
        self.WriteObject('6040','00','00000007',Node_ID,Show)
        time.sleep(0.1)
        self.WriteObject('6040','00','0000000f',Node_ID,Show)
        time.sleep(0.1)


    def Disenable_to_move(self,Node_ID = None,Show = False):
        if Node_ID == None:
            Node_ID = self.NodeID
        self.WriteObject('6040','00','00000000',Node_ID,Show)

    def Move_position(self,Position_dec,Node_ID = None,Show = False):
        if Node_ID == None:
            Node_ID = self.NodeID
            
        #Consult = self.ReadObject('6041','00',Node_ID,Show)
        Consult = 1
        if Consult != None:
            try:
                #Statusword = Consult[2]
                Statusword = '00000437'
                if Statusword == '00000437':
                    Hex_position = self.INT32_2_hex_str(Position_dec,FULL_4_Bytes=True)
                    Hex_position = Hex_position[2:len(Hex_position)]
                    self.WriteObject('607A','00',Hex_position,Node_ID,Show)
                    time.sleep(0.01)
                    self.WriteObject('6040','00','000000ff',Node_ID,Show)
                    time.sleep(0.01)
                    self.WriteObject('6040','00','0000000f',Node_ID,Show)
                    time.sleep(0.01)
                    
                elif Statusword == '00000037':
                    print('Epos4 is Moving the motor, Statusword: ' + Statusword)
                else:
                    print('Epos4 Not Enabled, Statusword: ' + Statusword)
            except Exception, e1:
                print ("Error data: " + str(e1))
        else:
            print('Error in Statusword consult')

        
        
