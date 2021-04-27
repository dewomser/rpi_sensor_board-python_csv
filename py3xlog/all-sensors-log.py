#!/usr/bin/env python3
import math
import time
import os
from ctypes import *
#cdll.LoadLibrary("./bcm2835.so")

sensor = CDLL("./sensor.so")

class mag3110:
		
	def __init__(self):

		if ( True == os.path.exists('mag_calibration.data')):
			f_cal = open("mag_calibration.data", "r")
			s = f_cal.readline()
			[self.x_off, self.y_off, self.z_off] = s.split()
			f_cal.close()
		else:
			self.x_off = -565
			self.y_off = 700
			self.z_off = 0
		
		if (0 == sensor.bcm2835_init()):
			print ("bcm3835 driver init failed.")
			return
		
	def writeRegister(self, register, value):
	    sensor.MAG3110_WRITE_REGISTER(register, value)

	def readRegister(self, register):
		return sensor.MAG3110_READ_REGISTER(register)
	
	def __str__(self):
		ret_str = ""
		(x, y, z) = self.getAxes()
		ret_str += "X: "+str(x) + "  "
		ret_str += "Y: "+str(y) + "  "
		ret_str += "Z: "+str(z)
		
		return ret_str

	def init(self):
		sensor.MAG3110_Init()
	def readRawData_x(self):
		return sensor.MAG3110_ReadRawData_x()

	def readRawData_y(self):
		return sensor.MAG3110_ReadRawData_y()

	def readRawData_z(self):
		return sensor.MAG3110_ReadRawData_z()

	def getAxes(self):
		x = self.readRawData_x()
		y = self.readRawData_y()
		z = self.readRawData_z()

		return (x, y, z)

	def readAsInt(self):
		x = self.readRawData_x() / 40
		y = self.readRawData_y() / 40 
		z = self.readRawData_z() / 40

		return (x, y, z)
		 		
	def getHeading(self):
		(x, y, z) = self.getAxes()
		
		heading = math.atan2((y-self.y_off), (x-self.x_off)) * 180/math.pi + 180
		
		return heading

	def calibrate(self, x, y, z):
		max_x = max(x)
		max_y = max(y)
		max_z = max(z)

		min_x = min(x)
		min_y = min(y)
		min_z = min(z)
		
		self.x_off = (max_x + min_x) / 2
		self.y_off = (max_y + min_y) / 2 
		self.z_off = 0 #(max_z + min_z) / 2
		
file1 = open("mag.csv", "w")		
mag = mag3110()
mag.init()


#---------------------------------------------------------------------

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


file2 = open("beschl.csv", "w")
		
mxa = mma8491q()
mxa.init()
mxa.enable()


#----------------------------------------------------------------------------------



sensor = CDLL("./sensor.so")

class mpl3115a2:
	def __init__(self):
		if (0 == sensor.bcm2835_init()):
			print ("bcm3835 driver init failed.")
			return
			
	def writeRegister(self, register, value):
	    sensor.MPL3115A2_WRITE_REGISTER(register, value)
	    
	def readRegister(self, register):
		return sensor.MPL3115A2_READ_REGISTER(register)

	def active(self):
		sensor.MPL3115A2_Active()

	def standby(self):
		sensor.MPL3115A2_Standby()

	def initAlt(self):
		sensor.MPL3115A2_Init_Alt()

	def initBar(self):
		sensor.MPL3115A2_Init_Bar()

	def readAlt(self):
		return sensor.MPL3115A2_Read_Alt()

	def readTemp(self):
		return sensor.MPL3115A2_Read_Temp()

	def setOSR(self, osr):
		sensor.MPL3115A2_SetOSR(osr);

	def setStepTime(self, step):
		sensor.MPL3115A2_SetStepTime(step)

	def getTemp(self):
		t = self.readTemp()
		t_m = (t >> 8) & 0xff;
		t_l = t & 0xff;

		if (t_l > 99):
			t_l = t_l / 1000.0
		else:
			t_l = t_l / 100.0
		return (t_m + t_l)

	def getAlt(self):
		alt = self.readAlt()
		alt_m = alt >> 8 
		alt_l = alt & 0xff
		
		if (alt_l > 99):
			alt_l = alt_l / 1000.0
		else:
			alt_l = alt_l / 100.0
			
		return self.twosToInt(alt_m, 16) + alt_l
	def getBar(self):
		alt = self.readAlt()
		alt_m = alt >> 6 
		alt_l = alt & 0x03
		
		if (alt_l > 99):
			alt_l = alt_l 
		else:
			alt_l = alt_l 

		return (self.twosToInt(alt_m, 18))

	def twosToInt(self, val, len):
		# Convert twos compliment to integer
		if(val & (1 << len - 1)):
			val = val - (1<<len)

		return val
file3 = open("druck.csv", "w")		
mpl = mpl3115a2()
timexa = 0
mpl.initAlt()
mpl.initBar()
mpl.active()
time.sleep(1)
while 1:
	
#	print "MPL3115:","\tAlt:",mpl.getAlt(),"\tBar:",mpl.getBar(),"\tTemp:", mpl.getTemp()
	
	alt1=mpl.getAlt()
	bar1=mpl.getBar()
	temp1=mpl.getTemp()


#	print timexa,x,y,z
    #timexa += 1   
	a = timexa, bar1, temp1
	file3.write("%s,%s,%s\n" % a)
#	printf ("%s,%s,%s\n" %a)
	
	


#print mag.x_off, mag.y_off, mag.z_off

	(x, y, z) = mag.readAsInt()
	#print "MAG3110:\tX.", x, "uT", "\tY.", y, "uT", "\tZ.", z, "uT" 
	#print mag.readRawData_x(), mag.readRawData_y(), mag.readRawData_z()
	#	print timexa,x,y,z
	a = timexa, x, y, z

	file1.write("%s,%s,%s,%s\n" % a)
#	printf ("%s,%s,%s,%s\n" %a)
	
	



	(x, y, z) = mxa.getAccelerometer()
#	print timexa,x,y,z
	a = timexa, x, y, z
	file2.write("%s,%s,%s,%s\n" % a)
#	printf ("%s,%s,%s,%s\n" %a)
	timexa += 1
	mxa.enable()
	time.sleep(0.5)
