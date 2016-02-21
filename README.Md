# Raspbian Safe

A simple python script supporting a *2 x 16* I2C screen, an *8 x 8* matrix keypad, and a 4 channel relay module. The program can run on bootup of a [RaspberryPi](https://www.raspberrypi.org/) to keep a locking circut closed until a code is entered. Support for lighting and or LED indicators. This could be installed on an electric locking door safe.

![alt tag](https://pbs.twimg.com/media/CbxbweiWIAArKEo.jpg:small)

- [Raspberry Pi v2](https://www.raspberrypi.org/products/raspberry-pi-2-model-b/), [Raspbian](https://www.raspbian.org/) OS, MicroSD Card
-  [4 pin I2C interface](http://goo.gl/j2pGl7) with 2 x 16 character dot matrix display
- [16 pin 8 x 8 numaric keypad](http://goo.gl/uhjbc0) with four alpha buttons
-  [6 pin 5v relay](http://goo.gl/RUHKiW) module
- [Electromagnetic](http://goo.gl/sdH5cf) or [solenoid](http://goo.gl/ycfzch) based door lock
- [12v RGB LED](http://goo.gl/R0RnQo) Lights
- [12v supply](http://goo.gl/A6PjdV) 
- [5v USB converter](http://goo.gl/lrsztp)
- Optional [12v battery](http://goo.gl/UadAzx) backup

Setup Raspbian and use SSH to clone the repository. Run the program with this command:
````
sudo python program.py
````

###### Pinout
Raspberry Pi pinout should follow this diagram. No resistors or circuitry are required if the correct components are selected.

[diagram]

**Correct pinout is important. Connecting pins incorrectly may cause harm to project components.**


###### Operation
*Run* `sudo python program.py`.
If the script has successfully started, the screen will read the time and two relays on the board will close. Relay 4 is the Lock controller, which stays locked until unlocked. The RBG light colours are connected to the other three relays.

- Type a code to open the Lock `1111`
- Pressing the `A` button will toggle lighting modes

Run `sudo dpkg-reconfigure tzdata` to set the system time which displays on the screen.

###### Startup 
Use `sudo crontab -e` to open the system cron table, then add a line to run the `startup.sh` file included in the repo. 
````
@reboot sh /home/pi/RaspbianSafe/startup.sh >/home/pi/RaspbianSafe/program.log 2>&1
````

###### Troubleshooting
Make sure Python and required Raspbian Python Libraries are installed and in the right locations. This script requires access to the latest versions of these modules:
- RPi GPIO > 0.6.1
- RPi I2C Driver

These are included in the package and may need to be copied to local Python dependency folders.
