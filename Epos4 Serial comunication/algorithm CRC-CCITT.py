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
