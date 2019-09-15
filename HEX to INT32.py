def INT32_2_hex_str(INT_32,FULL_4_Bytes=False):
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
