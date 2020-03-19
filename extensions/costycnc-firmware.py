#!/usr/bin/env python 

import inkex, serial, os

#copied from grbl_serial.py
def findPort():
	# Find a GRBL board connected to a USB port.
	try:
		from serial.tools.list_ports import comports
	except ImportError:
		comports = None
		return None
	if comports:
		comPortsList = list(comports())
		for port in comPortsList:
			desc = port[1].lower()
			isUsbSerial = "usb" in desc and "serial" in desc
			isArduino = "arduino" in desc 
			isCDC = "CDC" in desc 
			if isUsbSerial or isArduino or isCDC:
				return port[0]
				
	return None

class MyEffect(inkex.Effect):
	def __init__(self):
		inkex.Effect.__init__(self) 
		self.OptionParser.add_option("-t", "--boot", action="store", type="string",
									 dest="boot", default="boot-old", help=("Settings"))			
	def effect(self): 
		port=findPort()
		if (self.options.boot == "boot-old"): 
			os.system("avrdude -p m328p -b 57600 -P "+port+" -c arduino -U flash:w:refirmware_nou_dreapta.hex ")
		else :
			os.system("avrdude -p m328p -b 115200 -P "+port+" -c arduino -U flash:w:refirmware_nou_dreapta.hex ")
			
			
if __name__ == '__main__':
	e = MyEffect()
	e.affect()


