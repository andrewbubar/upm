import time, sys, signal, atexit
import sqlite3 as lite
import pyupm_pn532 as upmPn532
import pyupm_grove as grove
#import pyupm_i2clcd as lcd

BLUE_LED = 4
RED_LED = 5
GREEN_LED = 6

greenLED = grove.GroveLed(GREEN_LED)
blueLED = grove.GroveLed(BLUE_LED)
redLED = grove.GroveLed(RED_LED)

#myLCD = lcd.Lcm1602(13,12,11,10,9,8)
#lcdMessage = " "

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
#	myLCD.clear()
	greenLED.off()
	blueLED.off()
	redLED.off()
	con.close()
	sys.exit(0)
	
def getRFID():
	rfidData = []
	for i in range(uidSize.__getitem__(0)):
		rfidData.insert(i,uid.__getitem__(i))
	rfidNumber = ''
	for i in range(len(rfidData)):
		rfidNumber = str(rfidNumber) + str(rfidData[i])
	return rfidNumber

def registered():
	'''
	blueLED.off()
	redLED.on()
	myLCD.setCursor(0,0)
	myLCD.write("RFID already")
	myLCD.setCursor(1,0)
	myLCD.write("registered")
	time.sleep(1)
	myLCD.clear()
	blueLED.on()
	'''
	print ("RFID already registered")
	
def enterInfo():
	name = raw_input('Enter the name: ')
      	laser = raw_input('Laser Access? ')
      	printer = raw_input('Printer Access? ')
      	solder = raw_input('Solder Access? ')
	params = (rfidNumber, name, laser, printer, solder)
	cur.execute("INSERT INTO PERMISSIONS VALUES(?, ?, ?, ?, ?)", params)
	con.commit()
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

while (1):
	for i in range(7):
		uid.__setitem__(i, 0)
	if (myNFC.readPassiveTargetID(upmPn532.PN532.BAUD_MIFARE_ISO14443A,
                                      uid, uidSize, 2000)):
		# found a card
		rfidNumber = getRFID()
		cur.execute("SELECT * FROM PERMISSIONS where ID = ?", [rfidNumber])
		result = cur.fetchone()
		if result is not None:
			registered()
		else:
			enterInfo()
	else:
		waiting()
