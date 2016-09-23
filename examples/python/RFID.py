#!/usr/bin/python
# Authors: Andrew Bubar & Hunter Pickett, but mostly Andrew and the internet

import time, sys, signal, atexit
import pyupm_pn532 as upmPn532
import sqlite3 as lite
import pyupm_grove as grove
import pyupm_i2clcd as lcd
import datetime

BLUE_LED = 4
RED_LED = 5
GREEN_LED = 6

greenLED = grove.GroveLed(GREEN_LED)
blueLED = grove.GroveLed(BLUE_LED)
redLED = grove.GroveLed(RED_LED)

myLCD = lcd.Lcm1602(13,12,11,10,9,8)
lcdMessage = " "

relay = grove.GroveRelay(7)
relay.off()

con = lite.connect('makerspace.db')
cur = con.cursor()

blueLED.on()

# Instantiate an PN532 on I2C bus 0 (default) using gpio 3 for the
# IRQ, and gpio 2 for the reset pin.
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
	sys.exit(0)

def checkTable(rfidNumber):
    
        if len(rfidNumber) > 0:
            cur = con.cursor()
            cur.execute("SELECT * FROM PERMISSIONS where ID = ?", [rfidNumber])
            result = cur.fetchone()
            try:
                if (result[0] == rfidNumber):
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
            except TypeError:
                lcdMessage = "Sorry RFID is"
                lcdMessage2 = "not registered")
                myLCD.setCursor(0,0)
                myLCD.write(lcdMessage)
                myLCD.setCursor(1,0)
                myLCD.write(lcdMessage2)
                time.sleep(2)
                myLCD.clear()
def cutter(laser):
    
        if laser == 'Y' or laser == 'y':
            greenLED.on()
            lcdMessage = "Access Granted"
            myLCD.setCursor(0,0)
            myLCD.write(lcdMessage)
            time.sleep(2)
            myLCD.clear()
            startTime = datetime.datetime.today()
        else:
            redLED.on()
            lcdMessage = "Access Denied"
            myLCD.setCursor(0,0)
            myLCD.write(lcdMessage)
            time.sleep(2)
            myLCD.clear()
            redLED.off()
            # keep machine off
def cardCheck():
	for i in range(7):
		uid.__setitem__(i, 0)
	if (myNFC.readPassiveTargetID(upmPn532.PN532.BAUD_MIFARE_ISO14443A,
                                      uid, uidSize, 2000)):
		# found a card
		rfidData = []
		for i in range(uidSize.__getitem__(0)):
			rfidData.insert(i,uid.__getitem__(i))
		newRfidNumber = ''
		for i in range(len(rfidData)):
			newRfidNumber = str(newRfidNumber) + str(rfidData[i])
		return newRfidNumber
	else:
		newRfidNumber = '000000000'
		return newRfidNumber
		
def waiting():
	greenLED.off()
	redLED.off()
        lcdMessage = "Waiting for a"
        lcdMessage2 = "card . . .")
        myLCD.setCursor(0,0)
        myLCD.write(lcdMessage)
        myLCD.setCursor(1,0)
        myLCD.write(lcdMessage2)
        time.sleep(2)
        myLCD.clear()
        
def writeLCD2Line(message, message2, cursor, cursor2, sleep):
	myLCD.clear()
	myLCD.setCursor(cursor)
	myLCD.write(message)
	myLCD.setCursor(cursor2)
	myLCD.write(message2)
	time.sleep(sleep)

def writeLCD1Line(message, cursor, sleep):
	myLCD.clear()
	myLCD.setCursor(cursor)
	myLCD.write(message)
	time.sleep(sleep)
	
def sendData(ID, name, startTime, endTime):
	cur = con.cursor()
	values = [ID, name, startTime, endTime]
	cur.exectue("INSERT INTO USED VALUES(?,?,?,?)", values)
	con.commit()
	

# Register exit handlers
atexit.register(exitHandler)
signal.signal(signal.SIGINT, SIGINTHandler)


if (not myNFC.init()):
	print "init() failed"
	sys.exit(0)
"""
vers = myNFC.getFirmwareVersion()

if (vers):
	print "Got firmware version: %08x" % vers
else:
	print "Could not identify PN532"
	sys.exit(0)
"""

# Now scan and identify any cards that come in range (1 for now)

# Retry forever
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
		rfidData = []
		for i in range(uidSize.__getitem__(0)):
			rfidData.insert(i,uid.__getitem__(i))
		rfidNumber = ''
		for i in range(len(rfidData)):
			rfidNumber = str(rfidNumber) + str(rfidData[i])
		try:
			name, laser, printer, solder = checkTable(rfidNumber)
			startTime = str(datetime.datetime.today())
			cutter(laser) # laser is on
			while (1):
				newRfidNumber = cardCheck()
				if newRfidNumber == rfidNumber:
					myLCD.clear()
					lcdMessage = "Have fun cutting"
					myLCD.setCursor(0,0)
					myLCD.write(lcdMessage)
					time.sleep(1)
					continue
				else:
					num = 60
					while num > 0:
						newRfidNumber = cardCheck()
						if newRfidNumber == rfidNumber:
							break
						num = num - 1
						myLCD.clear()
						lcdMessage = "Place card or"
						lcdMessage2 = "%s sec left" %num
						myLCD.setCursor(0,0)  
						myLCD.write(lcdMessage)
						myLCD.setCursor(1,0)
						myLCD.write(lcdMesaage2)
						if num == 0:
							endTime = str(datetime.datetime.today())
							values = [rfidNumber, name, startTime, endTime]
							cur.execute("INSERT INTO USED VALUES(?,?,?,?)", values)
							con.commit()
							sendData(rfidNumber, name, startTime, endTime)
						continue
					break
				except:
					break
						
	else:
		waiting()
