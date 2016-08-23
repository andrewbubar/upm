import mraa, time
import pyupm_i2clcd as lcd

lcdMessage = " "
myLCD = lcd.Jhd1313m1(6, 0x3E, 0x62)

def loop():
  lcdMessage = "Hello, Hunter"
  myLCD.setCursor(0,1)
  myLCD.write(lcdMessage)
  time.sleep(1)
  
loop()
