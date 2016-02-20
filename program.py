#!/usr/bin/python3
import RPi_I2C_driver
import time
import datetime
import logging
import sys; sys.path.append('/home/pi/door/')
try:
	import RPi.GPIO as GPIO
except RuntimeError:
	print("Error importing RPi.GPIO!  This is probably because you need superuser privileges.  You can achieve this by using 'sudo' to run your script")

# Passcode
code = '1111';
request = '';

# LEDs
lights = 'Auto';

# Door
door = True;
open = 12;

# Initialize LCD module
lcd = RPi_I2C_driver.lcd();
lcd.lcd_clear();
lcd.backlight(0);

# Initialize Matrix Keypad
matrix = [ ['1','2','3','A'],
	   ['4','5','6','B'],
	   ['7','8','9','C'],
	   ['*','0','#','D'] ];

# GPIO Pins
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
cols = [40,38,36,32]
rows = [31,33,35,37]

relay = [11,12,15,16]

# Logging
logger = logging.getLogger('safe')
handle = logging.FileHandler('./safe.log')
logformat = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
handle.setFormatter(logformat)
logger.addHandler(handle)
logger.setLevel(logging.INFO)

for j in range(4):
	GPIO.setup(cols[j], GPIO.OUT)
	GPIO.setup(relay[j], GPIO.OUT)
	GPIO.output(relay[j], 1)
	GPIO.output(cols[j], 1)
	pass
for i in range(4):
	GPIO.setup(rows[i], GPIO.IN, pull_up_down = GPIO.PUD_UP)
	pass

# Main loop
while True:
        moment = time.time();
        now = datetime.datetime.now();
        date = now.strftime("%Y-%m-%d %H:%M");

        for x in xrange(4):
            GPIO.output(cols[x], 0)
            for y in xrange(4):
                if GPIO.input(rows[y]) == 0:
                    request = request + matrix[x][y]
                    while(GPIO.input(rows[y]) == 0):
                        pass

                pass
            GPIO.output(cols[x], 1)
            pass

        if lights == 'True':
            GPIO.output(11,0)
            GPIO.output(12,0)
            GPIO.output(15,0)
        else:
            if lights == 'False':
                GPIO.output(11,1)
                GPIO.output(12,1)
                GPIO.output(15,1)
            else:
                if lights == 'Auto':
                    GPIO.output(11,0)
                    GPIO.output(12,1)
                    GPIO.output(15,1)

        if door == True:
            GPIO.output(16,0)
        else:
            GPIO.output(16,1)

        if request != '':
            
            if request == 'A':
                request = '';
                if lights == 'True':
                    lights = 'Auto';
                    GPIO.output(11,0)
                    GPIO.output(12,1)
                    GPIO.output(15,1)
                    lcd.lcd_display_string("  LED Lighting  ", 1);
                    lcd.lcd_display_string("> Auto Lights   ", 2);

                    time.sleep(3)
                    lcd.lcd_clear();
                else:
                    if lights == 'Auto':
                        lights = 'False';
                        GPIO.output(11,1)
                        GPIO.output(12,1)
                        GPIO.output(15,1)
                        lcd.lcd_display_string("  LED Lighting  ", 1);
                        lcd.lcd_display_string("> Lights Off    ", 2);

                        time.sleep(3)
                        lcd.lcd_clear();
                    else:
                        if lights == 'False':
                            lights = 'True';
                            GPIO.output(11, 0)
                            GPIO.output(12, 0)
                            GPIO.output(15, 0)
                            lcd.lcd_display_string("LED Lighting    ", 1);
                            lcd.lcd_display_string("> Lights On     ", 2);
                            
                            time.sleep(3)
                            lcd.lcd_clear();
            else:
                length = len( request );
                display = '';
                for prepend in xrange(16):
                    if length < 15:
                        if int( (15-length)/2 ) >= prepend:
                            display = display + ' ';
                for i in range(0,length):
                    display = display + '.';
                    pass
                for append in xrange(16):
                    if len( display ) <= append:
                        display = display + ' ';
                    pass

                if request == code:
                    logger.info('Code Access Granted')
                    lcd.lcd_display_string(" Access Granted ", 1);
                    lcd.lcd_display_string("> Door Open     ", 2);
                    door = False;
                    logger.info('Door Opened')
                    GPIO.output(16, 1)
                    if lights == 'Auto':
                        GPIO.output(11, 1)
                        GPIO.output(12, 0)
                        GPIO.output(15, 1)
                        time.sleep(3)
                        GPIO.output(11, 0)
                        GPIO.output(12, 0)
                        GPIO.output(15, 0)
                    time.sleep(3)
                    lcd.lcd_display_string(date, 1);
                    time.sleep(open)
                    GPIO.output(16, 0)
                    request = '';
                    logger.info('Door Locked')
                    lcd.lcd_display_string("> Door Locked   ", 2);
                    if lights == 'Auto':
                        GPIO.output(12, 1)
                        GPIO.output(15, 1)
                    door = True;
                    lcd.lcd_clear()
                else:
                    lcd.lcd_display_string("   Enter Code   ", 1);
                    lcd.lcd_display_string(display, 2);
                    if len( request ) >= 4:
                        lcd.lcd_display_string(" Access Denied  ", 1);
                        lcd.lcd_display_string("> Log Saved     ", 2);
                        logger.error('Access Denied')
                        logger.info(request)
                        time.sleep(5)
                        request = ''
                        lcd.lcd_clear()
        else:
            lcd.lcd_display_string("  Current Time  ", 1)
            lcd.lcd_display_string(date, 2);

#elapsed = time.time() - moment
#time.sleep(1.-elapsed)
