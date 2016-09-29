import time, sys, signal, atexit
import sqlite3 as lite
import pyupm_pn532 as upmPn532
import pyupm_grove as grove
import pyupm_i2clcd as lcd

BLUE_LED = 4
RED_LED = 5
GREEN_LED = 6

greenLED = grove.GroveLed(GREEN_LED)
blueLED = grove.GroveLed(BLUE_LED)
redLED = grove.GroveLed(RED_LED)

myLCD = lcd.Lcm1602(13,12,11,10,9,8)
lcdMessage = " "

con = lite.connect('makerspace.db')
cur = con.cursor()

blueLED.on()

IRQ = 3
RST = 2
PN532_I2C_BUS = 6
PN532_DEFAULT_I2C_ADDR = (0x48 >> 1)
myNFC = upmPn532.PN532(IRQ, RST, PN532_I2C_BUS, PN532_DEFAULT_I2C_ADDR)

def SIGINTHandler(signum, frame):
	raise SystemExit

def exitHandler():
	print "Exiting"
	sys.exit(0)
	
atexit.register(exitHandler)
signal.signal(signal.SIGINT, SIGINTHandler)

if (not myNFC.init()):
	print "init() failed"
	sys.exit(0)
	
myNFC.setPassiveActivationRetries(0xff)

myNFC.SAMConfig()

uidSize = upmPn532.uint8Array(0)
uid = upmPn532.uint8Array(7)
print ("Scan RFID to update")

while (1):
	for i in range(7):
		uid.__setitem__(i, 0)
	if (myNFC.readPassiveTargetID(upmPn532.PN532.BAUD_MIFARE_ISO14443A,
                                      uid, uidSize, 2000)):
		rfidNumber = getRFID()
		checkTable(rfidNumber)
		if True:
			name, laser, printer, solder = fromTable(rfidNumber)
			print ("This RFID is registered for: " + name)
			print ("Laser Access: " + laser)
			print ("3D Printer Access: " + printer)
			print ("Solder Access: " + solder)
			question = 'Yes'
			while question == 'Yes':
				sel = raw_input("What would you like to update for this user? (Name, Laser, 3D Printer, or Solder)")
				if sel == 'Name':
					name = raw_input("What is the new name? ")
					params = name, rfidNumber
					cur.execute("UPDATE PERMISSIONS SET Name = ? WHERE ID = ?", params)
				elif sel == 'Laser':
					laser = raw_input("Y or N for Laser Cutter? ")
					params = laser, rfidNumber
					cur.execute("UPDATE PERMISSIONS SET Laser = ? WHERE ID = ?", params)
				elif sel == '3D Printer':
					printer = raw_input("Y or N for 3D Printer? ")
					params = printer, rfidNumber
					cur.execute("UPDATE PERMISSIONS SET Printer = ? WHERE ID = ?", params)
				elif sel == 'Solder':
					solder = raw_input("Y or N for Solder? ")
					params = solder, rfidNumber
					cur.execute("UPDATE PERMISSIONS SET Solder = ? WHERE ID = ?", params)
				question = raw_input("Would you like to update another machine? (Yes or No)")
			con.commit()
			con.close()
			blueLED.off()
			sys.exit(0)
		else:
			print ("RFID is not registered")
		result = cur.fetchone()
		try:
			print ("This RFID is registered for: " + result[1])
			if result is not None:
				sel = raw_input("What would you like to update for this user? ")
				if sel == 'Name':
			 		name = raw_input("What is the new name? ")
		  	 		params = name, rfidNumber
					cur.execute("UPDATE PERMISSIONS SET Name = ? WHERE ID = ?", params)
				if sel == 'Laser':
					laser = raw_input("Y or N for Laser Cutter? ")						params = laser, rfidNumber
			  		cur.execute("UPDATE PERMISSIONS SET Laser = ? WHERE ID = ?", params)
				if sel == 'Printer':
		  	 		printer = raw_input("Y or N for 3-D Printer? ")
					params = printer, rfidNumber
		 			cur.execute("UPDATE PERMISSIONS SET Printer = ? WHERE ID = ?", params)
				if sel == 'Solder':
					solder = raw_input("Y or N for Soldering Machine? ")
			 		params = solder, rfidNumber
			 		cur.execute("UPDATE PERMISSIONS SET Solder = ? WHERE ID = ?", params)
				con.commit()
				con.close()
				blueLED.off()
				sys.exit(0)
				
		except:
			print ("RFID is not registered")
	else:
		waiting()
