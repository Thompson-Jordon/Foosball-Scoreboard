#!/usr/bin/env python3
import RPi.GPIO as GPIO
import time

yellow_score = 0
black_score = 0
yellow_games = 0
black_games = 0

YELLOW_INPUT = 5
BLACK_INPUT = 6
RESET = 12

YELLOW_GAME_1 = 13
YELLOW_GAME_2 = 19
YELLOW_GAME_3 = 26

BLACK_GAME_1 = 16
BLACK_GAME_2 = 20
BLACK_GAME_3 = 21

YELLOW_SDI   = 17
YELLOW_RCLK  = 18
YELLOW_SRCLK = 27

BLACK_SDI   = 22
BLACK_RCLK  = 23
BLACK_SRCLK = 24

segCode = [0x3f,0x06,0x5b,0x4f,0x66,0x6d]

def setup():
	GPIO.setmode(GPIO.BCM)       # Numbers GPIOs by BCM
	GPIO.setup(YELLOW_INPUT, GPIO.IN, pull_up_down=GPIO.PUD_UP)    # Set BtnPin's mode is input, and pull up to high level(3.3V)
	GPIO.setup(BLACK_INPUT, GPIO.IN, pull_up_down=GPIO.PUD_UP)    # Set BtnPin's mode is input, and pull up to high level(3.3V)
	GPIO.setup(RESET, GPIO.IN, pull_up_down=GPIO.PUD_UP)    # Set BtnPin's mode is input, and pull up to high level(3.3V)
	GPIO.setup(YELLOW_GAME_1, GPIO.OUT)
	GPIO.output(YELLOW_GAME_1, GPIO.HIGH) 
	GPIO.setup(YELLOW_GAME_2, GPIO.OUT)
	GPIO.output(YELLOW_GAME_2, GPIO.HIGH) 
	GPIO.setup(YELLOW_GAME_3, GPIO.OUT)
	GPIO.output(YELLOW_GAME_3, GPIO.HIGH) 
	GPIO.setup(BLACK_GAME_1, GPIO.OUT)
	GPIO.output(BLACK_GAME_1, GPIO.HIGH) 
	GPIO.setup(BLACK_GAME_2, GPIO.OUT)
	GPIO.output(BLACK_GAME_2, GPIO.HIGH) 
	GPIO.setup(BLACK_GAME_3, GPIO.OUT)
	GPIO.output(BLACK_GAME_3, GPIO.HIGH)
	GPIO.setup(YELLOW_SDI, GPIO.OUT)
	GPIO.setup(YELLOW_RCLK, GPIO.OUT)
	GPIO.setup(YELLOW_SRCLK, GPIO.OUT)
	GPIO.output(YELLOW_SDI, GPIO.LOW)
	GPIO.output(YELLOW_RCLK, GPIO.LOW)
	GPIO.output(YELLOW_SRCLK, GPIO.LOW)
	GPIO.setup(BLACK_SDI, GPIO.OUT)
	GPIO.setup(BLACK_RCLK, GPIO.OUT)
	GPIO.setup(BLACK_SRCLK, GPIO.OUT)
	GPIO.output(BLACK_SDI, GPIO.LOW)
	GPIO.output(BLACK_RCLK, GPIO.LOW)
	GPIO.output(BLACK_SRCLK, GPIO.LOW)


def add_point_yellow(ev=None):
	global yellow_score
	global black_score
	global yellow_games
	if yellow_score >= 4:
		yellow_score = 0
		black_score = 0
		yellow_games += 1
	else:
		yellow_score += 1
	render()


def add_point_black(ev=None):
	global black_score
	global yellow_score
	global black_games
	if black_score >= 4:
		black_score = 0
		yellow_score = 0
		black_games += 1
	else:
		black_score += 1
	render()

def render_yellow_score(dat):
	for bit in range(0, 8):	
		GPIO.output(YELLOW_SDI, 0x80 & (dat << bit))
		GPIO.output(YELLOW_SRCLK, GPIO.HIGH)
		time.sleep(0.001)
		GPIO.output(YELLOW_SRCLK, GPIO.LOW)
	GPIO.output(YELLOW_RCLK, GPIO.HIGH)
	time.sleep(0.001)
	GPIO.output(YELLOW_RCLK, GPIO.LOW)

def render_black_score(dat):
	for bit in range(0, 8):	
		GPIO.output(BLACK_SDI, 0x80 & (dat << bit))
		GPIO.output(BLACK_SRCLK, GPIO.HIGH)
		time.sleep(0.001)
		GPIO.output(BLACK_SRCLK, GPIO.LOW)
	GPIO.output(BLACK_RCLK, GPIO.HIGH)
	time.sleep(0.001)
	GPIO.output(BLACK_RCLK, GPIO.LOW)


def render_games():
	global yellow_games
	global black_games
	GPIO.output(YELLOW_GAME_1, yellow_games < 1)
	GPIO.output(YELLOW_GAME_2, yellow_games < 2)
	GPIO.output(YELLOW_GAME_3, yellow_games < 3)
	GPIO.output(BLACK_GAME_1, black_games < 1)
	GPIO.output(BLACK_GAME_2, black_games < 2)
	GPIO.output(BLACK_GAME_3, black_games < 3)

def reset(ev=None):
	global yellow_games, yellow_score, black_games, black_score
	yellow_games = 0
	yellow_score = 0
	black_games = 0
	black_score = 0
	render()

def render():
	global yellow_score
	global black_score
	render_yellow_score(segCode[yellow_score])
	render_black_score(segCode[black_score])
	render_games()


def loop():
	GPIO.add_event_detect(YELLOW_INPUT, GPIO.FALLING, callback=add_point_yellow, bouncetime=2000) # wait for falling and set bouncetime to prevent the callback function from being called multiple times when the button is pressed
	GPIO.add_event_detect(BLACK_INPUT, GPIO.FALLING, callback=add_point_black, bouncetime=2000) # wait for falling and set bouncetime to prevent the callback function from being called multiple times when the button is pressed
	GPIO.add_event_detect(RESET, GPIO.FALLING, callback=reset, bouncetime=200) # wait for falling and set bouncetime to prevent the callback function from being called multiple times when the button is pressed
	while True:
		time.sleep(1)   # Don't do anything

def destroy():
	GPIO.output(YELLOW_INPUT, GPIO.HIGH)     # led off
	GPIO.output(BLACK_INPUT, GPIO.HIGH)     # led off
	GPIO.output(RESET, GPIO.HIGH)     # led off
	GPIO.cleanup()  

if __name__ == '__main__':     # Program start from here
	setup()
	reset()
	try:
		loop()
	except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
		destroy()