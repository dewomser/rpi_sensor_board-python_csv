#!/usr/bin/env python
import math
import time
from ctypes import *
#cdll.LoadLibrary("./bcm2835.so")

sensor = CDLL("./sensor.so")

class MMA8491Q_DATA(Structure):
	_fields_  = [("Xout", c_int16),
	("Yout", c_int16),
	("Zout", c_int16)]

class mma8491q:
	def __init__(self):
		if (0 == sensor.bcm2835_init()):
			print ("bcm3835 driver init failed.")
			return	

	def init(self):
		sensor.MMA8491Q_Init()
		
	def enable(self):
		sensor.MMA8491Q_Enable()

	def disEnable(self):
		sensor.MMA8491Q_DisEnable()
		
	def writeRegister(self, register, value):
		sensor.MMA8491Q_WRITE_REGISTER()

	def readRegister(self, register):
		return sensor.MMA8491Q_READ_REGISTER()

	def read(self, data):
		sensor.MMA8491_Read(data)	

	def getAccelerometer(self):
		data = 	MMA8491Q_DATA()
		pdata = pointer(data)
		self.read(pdata)
		return (data.Xout, data.Yout, data.Zout);
		
	def __str__(self):
		ret_str = ""
		(x, y, z) = self.getAccelerometer()
		ret_str += "X: "+str(x) + "  "
		ret_str += "Y: "+str(y) + "  "
		ret_str += "Z: "+str(z)
		
		return ret_str
		
	def twosToInt(self, val, len):
		# Convert twos compliment to integer
		if(val & (1 << len - 1)):
			val = val - (1<<len)

		return val


file = open("beschl.csv", "w")
		
mxa = mma8491q()
timexa = 0
mxa.init()
mxa.enable()

while 1:
	(x, y, z) = mxa.getAccelerometer()
#	print timexa,x,y,z
	a = timexa, x, y, z
	file.write("%s,%s,%s,%s\n" % a)
#	printf ("%s,%s,%s,%s\n" %a)
	timexa += 1
	mxa.enable()
	time.sleep(0.5)

