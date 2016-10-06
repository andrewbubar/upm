import time, sys, signal, atexit
import sqlite3 as lite
import pyupm_pn532 as upmPn532
#import pyupm_grove as grove
#import pyupm_i2clcd as lcd
'''
BLUE_LED = 4
RED_LED = 5
GREEN_LED = 6

greenLED = grove.GroveLed(GREEN_LED)
blueLED = grove.GroveLed(BLUE_LED)
redLED = grove.GroveLed(RED_LED)

myLCD = lcd.Lcm1602(13,12,11,10,9,8)
lcdMessage = " "
'''

con = lite.connect('makerspace.db')
cur = con.cursor()

#blueLED.on()

IRQ = 3
RST = 2
PN532_I2C_BUS = 6
PN532_DEFAULT_I2C_ADDR = (0x48 >> 1)
myNFC = upmPn532.PN532(IRQ, RST, PN532_I2C_BUS, PN532_DEFAULT_I2C_ADDR)

def SIGINTHandler(signum, frame):
	raise SystemExit

def exitHandler():
	print "Exiting"
	'''
	myLCD.clear()
	greenLED.off()
	blueLED.off()
	redLED.off()
	'''
	con.close()
	sys.exit(0)
	
def waiting():
	print ("Waiting for a card")
	'''
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
	'''
	
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
		result = cur.fetchone()
		try:
			if result[0] == number:
				return True
		except TypeError:
			return False
		
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
		'''
		lcdMessage = "Hello " + first + "!"
		myLCD.setCursor(0,0)
		myLCD.write(lcdMessage)
		time.sleep(1)
		myLCD.clear()
		'''
		return name, laser, printer, solder
	
def displayRFID(name, laser, printer, solder):
	print ("This RFID is registered for: " + name)
	print ("Laser Access: " + laser)
	print ("3D Printer Access: " + printer)
	print ("Solder Access: " + solder)
	
def updateRFID():
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
	if question == 'Yes':
		return True
	else:
		return False

	
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
		inDatabase = checkTable(rfidNumber)
		if inDatabase == True:
			name, laser, printer, solder = fromTable(rfidNumber)
			displayRFID(name, laser, printer, solder)
			update = True
			while update == True:
				TF = updateRFID()
			con.commit()
			sys.exit(0)
		else:
			print ("RFID is not registered")
		
	else:
		waiting()
