import RPi_I2C_driver
import RPi.GPIO as GPIO
from time import *
import datetime

code = '1111';
request = '';

# Initialize LCD module
lcd = RPi_I2C_driver.lcd();
lcd.lcd_clear();
lcd.backlight(0);
sleep(0.25)

# Initialize Matrix Keypad
matrix = [ [1,2,3,'A'],
		   [4,5,6,'B'],
		   [7,8,9,'C'],
		   ['*',0,'#','D'] ];



# Initalize Relay GPIO 
relays = [04,17,27,22]
GPIO.setup(04, GPIO.OUT)

while lcd:
	now = datetime.datetime.now();
	date = now.strftime("%Y-%m-%d %H:%M");

	if request != '':
		length = len( request );
		display = '';
		for prepend in range(1, 16):
			if (16-length)/2 >= prepend:
				display = display + ' ';
			pass
		pass
		for i in range(0,length):
			display = display + '*';
		pass
		lcd.lcd_display_string("   Enter Code   ", 1);
		lcd.lcd_display_string(display, 2);
	else:
		lcd.lcd_display_string("  Current Time  ", 1)
		lcd.lcd_display_string(date, 2);
	pass

	

	sleep(1)
pass

sleep(60);
lcd.backlight(0);
