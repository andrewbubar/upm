#!/usr/bin/python
# Authors: Andrew Bubar & Hunter Pickett, but mostly Andrew and the internet

# import necessary modules
import time, sys, signal, atexit
import pyupm_pn532 as upmPn532
import sqlite3 as lite
import pyupm_grove as grove
import pyupm_i2clcd as lcd
import datetime

# declare LED pins
BLUE_LED = 4
RED_LED = 5
GREEN_LED = 6

# initialize LEDs
greenLED = grove.GroveLed(GREEN_LED)
blueLED = grove.GroveLed(BLUE_LED)
redLED = grove.GroveLed(RED_LED)

# initialize LCD
myLCD = lcd.Lcm1602(13,12,11,10,9,8)
lcdMessage = " "

# initialize power relay
relay = grove.GroveRelay(7)
relay.off()

# connect to database and set cursor
con = lite.connect('makerspace.db')
cur = con.cursor()

blueLED.on() # turn on blue LED

# set IRQ, RST, I2C bus, ADDR and initialize RFID reader
IRQ = 3
RST = 2
PN532_I2C_BUS = 6
PN532_DEFAULT_I2C_ADDR = (0x48 >> 1)
myNFC = upmPn532.PN532(IRQ, RST, PN532_I2C_BUS, PN532_DEFAULT_I2C_ADDR)

## Exit handlers ##
# This stops python from printing a stacktrace when you hit control-C
def SIGINTHandler(signum, frame):
	raise SystemExit

# This lets you run code on exit
def exitHandler():
	print "Exiting"
	myLCD.clear()
	greenLED.off()
	blueLED.off()
	redLED.off()
	con.close()
	relay.off()
	sys.exit(0)

# when no RFID card is scanned
def waiting():
	greenLED.off()
	redLED.off()
  	lcdMessage = "Waiting for a"
  	lcdMessage2 = "card . . ."
  	myLCD.setCursor(0,0)
	myLCD.write(lcdMessage)
	myLCD.setCursor(1,0)
	myLCD.write(lcdMessage2)
	time.sleep(2)
	myLCD.clear()
	relay.off()

def getRFID():
	rfidData = []
	for i in range(uidSize.__getitem__(0)):
		rfidData.insert(i,uid.__getitem__(i))
	rfidNumber = ''
	for i in range(len(rfidData)):
		rfidNumber = str(rfidNumber) + str(rfidData[i])
	return rfidNumber


def checkTable(number):
	if len(number) > 0:
		cur.execute("SELECT * FROM PERMISSIONS WHERE ID = ?", [number])
		if TypeError:
			return False
		else:
			return True

def fromTable(number):
	if len(number) > 0:
		cur.execute("SELECT * FROM PERMISSIONS WHERE ID = ?", [number])
		result = cur.fetchone()
		name = result[1]
    		name = name.encode("utf-8")
    		first, last = name.split()
		laser = result[2]
		printer = result[3]
		solder = result[4]
		lcdMessage = "Hello " + first + "!"
		myLCD.setCursor(0,0)
		myLCD.write(lcdMessage)
		time.sleep(1)
		myLCD.clear()
		return name, laser, printer, solder

def machine(device):
	if device == 'Y' or 'y':
		greenLED.on()
    		lcdMessage = "Access Granted"
    		myLCD.setCursor(0,0)
    		myLCD.write(lcdMessage)
    		time.sleep(1)
    		myLCD.clear()
		relay.on()
		return True
	else:
		redLED.on()
    		lcdMessage = "Access Denied"
    		myLCD.setCursor(0,0)
    		myLCD.write(lcdMessage)
    		time.sleep(1)
    		myLCD.clear()
    		redLED.off()
		relay.off()
		return False

def keepMachineOn():
	myLCD.clear()
	lcdMessage = "Have fun cutting"
	myLCD.setCursor(0,0)
	myLCD.write(lcdMessage)
	time.sleep(5)

def countdown(number):
	num = 10
	while num > 0:
		if (myNFC.readPassiveTargetID(upmPn532.PN532.BAUD_MIFARE_ISO14443A,
					      uid, uidSize, 2000)):
			newRfidNumber = getRFID()
			if newRfidNumber == number:
				print "countdown return true"
				return True
			else:
				num = num - 1
				myLCD.clear()
				lcdMessage = "Place same card"
				lcdMessage2 = " or %s sec left" %num
				myLCD.setCursor(0,0)
				myLCD.write(lcdMessage)
				myLCD.setCursor(1,0)
				myLCD.write(lcdMessage2)
				time.sleep(1)
		else:
			num = num - 1
			myLCD.clear()
			lcdMessage = "Place same card"
			lcdMessage2 = " or %s sec left" %num
			myLCD.setCursor(0,0)
			myLCD.write(lcdMessage)
			myLCD.setCursor(1,0)
			myLCD.write(lcdMessage2)
	else:
		#print "countdown return False"
		return False
		
def sendData(ID, name, startTime, endTime):
	values = [ID, name, startTime, endTime]
	cur.execute("INSERT INTO USED VALUES(?,?,?,?)", values)
	con.commit()
	#print "data sent"
	
	
if (not myNFC.init()):
	print "init() failed"
	sys.exit(0)
	
atexit.register(exitHandler)
signal.signal(signal.SIGINT, SIGINTHandler)

# Retry forever
myNFC.setPassiveActivationRetries(0xff)

myNFC.SAMConfig()

uidSize = upmPn532.uint8Array(0)
uid = upmPn532.uint8Array(7)
	
	
while (1):
 	for i in range(7):
		uid.__setitem__(i,0)
	if (myNFC.readPassiveTargetID(upmPn532.PN532.BAUD_MIFARE_ISO14443A,
                                                uid, uidSize, 2000)):
		rfidNumber = getRFID()
		inDatabase = checkTable(rfidNumber)
		if inDatabase == True:
			#print "RFID is registered"
			name, laser, printer, solder = fromTable(rfidNumber)
      			access = machine(laser)
			if access == True:
      				#print "start timne"
				startTime = str(datetime.datetime.today())
				machineOn = True
      				while(machineOn == True):
        				#print "machine is on"
					if (myNFC.readPassiveTargetID(upmPn532.PN532.BAUD_MIFARE_ISO14443A,
								      uid, uidSize, 2000)):
          					newRfidNumber = getRFID()
						#print "got RFID"
          					if newRfidNumber == rfidNumber:
            						keepMachineOn()
						else:
							#print "inner countdown"
							machineOn = countdown(rfidNumber)
					else:
						#print "outer countdown"
						machineOn = countdown(rfidNumber)
				#else:
				#print "outside while loop"
				relay.off()
				endTime = str(datetime.datetime.today())
				sendData(rfidNumber, name, startTime, endTime)
			else:
				print "No access"
		else:
			print "RFID is not registered"
	else:
     		waiting()
		#print "waiting"
