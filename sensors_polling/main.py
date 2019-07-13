# -*- coding: utf-8 -*-
from os import system
from m4m_imu import *
from m4m_utils import *
from m4m_obd import *
from m4m_gsm import *

polling_delay = 1
print(cur_date(), "Power on\n")
print("Current polling delay time: {}s".format(polling_delay))


#redOn()

#IMU START -> thread
imu_ev = threading.Event()
imu_t = threading.Thread(target=imu_connect, args=())
imu_t.do_run = True
imu_t.start()
imu_ev.set()

#GSM START
gsm_con = gsm_start()

#sim check

#eth check

#obd START
obd_con = obd_start()
#if not obd_con.is_connected():
	#gsm_sendSMS(gsm_con, PHONE, MSG_OBD_DISCONNECT_ENG)

mac = getMAC()
data = {}
lat, lon = 0, 0

#nginx START
system("sudo service nginx start")


#gsm_call(gsm_con, PHONE)
#beep()

try:
	while True:
		if obd_con.is_connected():
			try:
				data = obd_read(obd_con)
				json_send(1, data)
			except:
				print("Failed reading data from obd!")

		if gsm_con:
			try:
				lat, lon = gsm_getGPS(gsm_con)
				json_send(2, {'lat': lat, 'lon': lon})
			except:
				print("Failed reading data from gps!")

		time.sleep(polling_delay)
except KeyboardInterrupt:
	if gsm_con is not None:
		gsm_con.close()
finally:
	imu_t.do_run = False
	if gsm_con:
		gsm_con.close()
