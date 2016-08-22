#!/usr/bin/python
# Authors: Andrew Bubar & Hunter Pickett

import time, sys, signal, atexit
import pyupm_pn532 as upmPn532
import sqlite3 as lite
import pyupm_grove as grove

GREEN_LED = 4
BLUE_LED = 5
RED_LED = 6

greenLED = grove.GroveLed(GREEN_LED)
blueLED = grove.GroveLed(BLUE_LED)
redLED = grove.GroveLed(RED_LED)

con = lite.connect('makerspace.db')

blueLED.on()
# Instantiate an PN532 on I2C bus 0 (default) using gpio 3 for the
# IRQ, and gpio 2 for the reset pin.
myNFC = upmPn532.PN532(3, 2)

## Exit handlers ##
# This stops python from printing a stacktrace when you hit control-C
def SIGINTHandler(signum, frame):
	raise SystemExit

# This lets you run code on exit
def exitHandler():
	print "Exiting"
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
                    laser = result[2]
                    printer = result[3]
                    solder = result[4]
                    print ("Hello " + name + "!")
                    return name, laser, printer, solder
            except TypeError:
                print ("Sorry RFID is not registered")
def cutter(laser):
    
        if laser == 'Y' or laser == 'y':
            # GRIO.output(TRANSISTOR, True)
            greenLED.on()
            time.sleep(2)
            print ("Access granted")
            greenLED.off()
        else:
            redLED.on()
            time.sleep(2)
            print ("You do not have access")
            redLED.off()
            # keep machine off

# Register exit handlers
atexit.register(exitHandler)
signal.signal(signal.SIGINT, SIGINTHandler)


if (not myNFC.init()):
	print "init() failed"
	sys.exit(0)

vers = myNFC.getFirmwareVersion()

if (vers):
	print "Got firmware version: %08x" % vers
else:
	print "Could not identify PN532"
	sys.exit(0)

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
		print "Found a card: UID len", uidSize.__getitem__(0)
		print "UID: ",
		for i in range(uidSize.__getitem__(0)):
			print "%02x" % uid.__getitem__(i),
			rfidData.insert(i,uid.__getitem__(i))
		rfidNumber = ''
		for i in range(len(rfidData)):
			rfidNumber = str(rfidNumber) + str(rfidData[i])
		name, laser, printer, solder = checkTable(rfidNumber)
		cutter(laser)
		time.sleep(1)
	else:
		print "Waiting for a card...\n"
