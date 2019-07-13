# -*- coding: utf-8 -*-
import serial
import time
from m4m_utils import cur_date
from termcolor import colored

PHONE = "+79672518797"
MSG_OBD_DISCONNECT_ENG = "Attention! OBD not connected!"
MSG_OBD_DISCONNECT_RU = u"Внимание! OBD разъем не подключен!"

def gsm_start():
    print(cur_date(), "Starting GSM...")

    try:
        port = serial.Serial("/dev/ttyS0", baudrate=115200, timeout=1)
    except serial.SerialException:
        print(cur_date(), colored("GSM port not opened\n", 'red'))
        return None
    else:
        port.write('AT+CGNSPWR=1\r\n'.encode('utf-8')) #Glonass power on
        rcv = port.read(100)
        #print(rcv)

        port.write('AT+CGNSIPR=115200\r\n'.encode('utf-8'))
        rcv = port.read(100)
        #print(rcv)

        port.write('AT+CGNSTST=1\r\n'.encode('utf-8')) #print NMEA data 
        rcv = port.read(100)
        #print(rcv)

        port.write('AT+CGNSINF\r\n'.encode('utf-8')) #last package NMEA data
        rcv = port.read(200)
        #print(rcv)
        if rcv == b"":
            print(cur_date(), colored("GSM port not opened\n", 'red'))
            return None            
        else:
            print(cur_date(), "GSM started\n")

        return port

def gsm_getGPS(port):
    lat, lon = 0, 0
    while True:
        fd = port.read(200)

        if b'$GNRMC' in fd:
            idx = fd.find(b'$GNRMC')
            dif = len(fd) - idx
            b_data, fd1 = b'', b''

            if dif < 46:
                fd1 = port.read(200)
                b_data = fd[idx:] + fd1[:46-dif]
            else:
                b_data = fd[idx:idx+46]
            
            lat, lon = gsm_getloc(b_data)
            break
    return lat, lon

def gsm_getloc(data):
    idx = data.find(b'V')

    if idx == -1:
        idx = data.find(b'A')
        lat_deg = int(data[idx+2:idx+4])
        lat_remainder = data[idx+4:idx+13]
        lon_deg = int(data[idx+16:idx+19])
        lon_remainder = data[idx+19:idx+28]
        lat = lat_deg + float(lat_remainder) / 60
        lon = lon_deg + float(lon_remainder) / 60
        return lat, lon
    else:
        return 0, 0

def gsm_sendSMS(port, phone, text):
    data = ""
    num = 0
    W_buff = ["AT\r\n", "AT+CMGF=1\r\n", "AT+CSCA=\"+79262909090\"\r\n", "AT+CMGS=\""+phone+"\"\r\n",text]
    port.write(W_buff[0].encode('utf-8'))
    port.flushInput()
    while num < 4:
        while port.inWaiting() > 0:
            data += port.read(port.inWaiting()).decode('utf-8')
        if data != "":
            if num < 3:
                time.sleep(1)
                port.write(W_buff[num+1].encode('utf-8'))
            if num == 3:
                time.sleep(0.5)
                port.write(W_buff[4].encode('utf-8'))
                port.write("\x1a\r\n".encode('utf-8'))# 0x1a : send   0x1b : Cancel send
            num =num +1
            data = ""

def gsm_call(port,phone):
	W_buf_logoin = "AT+CREG?\r\n"
	W_buf_phone =  "ATD"+phone+";\r\n"
	port.write(W_buf_logoin.encode('utf-8'))

	port.flushInput()
	data = ""

	st = 1

	while st:
		while port.inWaiting() > 0:
			data += port.read(port.inWaiting()).decode('utf-8')
			time.sleep(0.0001)
		if data != "":
			if "CREG" in data:
				print(cur_date(), "Calling: "+phone)
				port.write(W_buf_phone.encode('utf-8'))

			if "NO CARRIER" in data:
				print(cur_date(), "Call completed: "+phone)
				st = 0
			data = ""	

#def gsm_getSMS() for command?
