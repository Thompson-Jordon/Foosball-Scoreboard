#!/usr/bin/env python

import RPi.GPIO as GPIO
import time

PIR_OUT_PIN = 3    # pin11
LIGHT = 13

def setup():
	GPIO.setmode(GPIO.BOARD)       # Numbers GPIOs by physical location
	GPIO.setup(PIR_OUT_PIN, GPIO.IN)  

def loop():
	while True:
		if GPIO.input(PIR_OUT_PIN) == GPIO.LOW:
			print '...Movement not detected!'
		else:
			print 'Movement detected!...'

def destroy():
	GPIO.cleanup()                     # Release resource

if __name__ == '__main__':     # Program start from here
	setup()
	try:
		loop()
	except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
		destroy()


# import RPi.GPIO as GPIO
# import time

# GPIO.setmode(GPIO.BCM)

# GPIO.setup(3, GPIO.IN) #PIR
# GPIO.setup(13, GPIO.OUT) #BUzzer
# GPIO.output(13, True)

# try:
#     time.sleep(2) # to stabilize sensor
#     while True:
#         if GPIO.input(3):
#             GPIO.output(13, False)
#             time.sleep(0.5) #Buzzer turns on for 0.5 sec
#             GPIO.output(13, True)
#             print("Motion Detected...")
#             time.sleep(5) #to avoid multiple detection
#         time.sleep(0.1) #loop delay, should be less than detection delay

# except:
#     GPIO.cleanup()