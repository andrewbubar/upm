import serial, time, sys
import sqlite3 as lite
import pyupm_pn532 as upmPn532
import pyupm_grove as grove

BLUE_LED = 4
RED_LED = 5
GREEN_LED = 6

greenLED = grove.GroveLed(GREEN_LED)
blueLED = grove.GroveLed(BLUE_LED)
redLED = grove.GroveLed(RED_LED)

myLCD = lcd.Lcm1602(13,12,11,10,9,8)
lcdMessage = " "

con = lite.connect('makerspace.db')

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
		# found a card
		rfidData = []
		for i in range(uidSize.__getitem__(0)):
			rfidData.insert(i,uid.__getitem__(i))
		rfidNumber = ''
		for i in range(len(rfidData)):
			rfidNumber = str(rfidNumber) + str(rfidData[i])
			greenLED.on()
			time.sleep(1)
			greenLED.off()
						cur = con.cursor()
			sel = print("What would you like to update for this user?")
			if sel == 'Name':
			  str(name) = print("What is the new name?")
			  cur.execute("UPDATE PERMISSIONS SET Name = name WHERE ID = rfidNumber")
			if sel == 'Laser':
			  str(laser) = print("Y or N for Laser Cutter?")
			  cur.execute("UPDATE PERMISSIONS SET Laser = laser WHERE ID = rfidNumber")
			if sel == 'Printer':
			  str(printer) = print("Y or N for 3-D Printer?")
			  cur.execute("UPDATE PERMISSIONS SET Printer = printer WHERE ID = rfidNumber")
			if sel == 'Solder':
			  str(solder) = print("Y or N for Soldering Machine?")
			  cur.execute("UPDATE PERMISSIONS SET Solder = solder WHERE ID = rfidNumber")
			con.commit()
			con.close()
			blueLED.off()
			sys.exit(0)
	else:
		print "Waiting for a card...\n"
