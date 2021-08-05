#!/usr/bin/env python3
import RPi.GPIO as GPIO
import time


press_count = 0
start_time = None
history = []


class Team:
    def __init__(self, color) -> None:
        self.color = color
        self.score = 0
        self.games = 0


class Game:
    def __init__(self, team_one_score, team_two_score) -> None:
        self.team_one_score = team_one_score
        self.team_two_score = team_two_score


team_one = Team("yellow")
team_two = Team("black")

game_log = []

YELLOW_INPUT = 5
BLACK_INPUT = 6
RESET = 12

YELLOW_GAME_1 = 13
YELLOW_GAME_2 = 19
YELLOW_GAME_3 = 26

BLACK_GAME_1 = 16
BLACK_GAME_2 = 20
BLACK_GAME_3 = 21

YELLOW_SDI = 17
YELLOW_RCLK = 18
YELLOW_SRCLK = 27

BLACK_SDI = 22
BLACK_RCLK = 23
BLACK_SRCLK = 24

segCode = [0x3F, 0x06, 0x5B, 0x4F, 0x66, 0x6D,0x7d,0x07,0x7f]


def setup():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)  # Numbers GPIOs by BCM
    GPIO.setup(
        YELLOW_INPUT, GPIO.IN, pull_up_down=GPIO.PUD_UP
    )  # Set BtnPin's mode is input, and pull up to high level(3.3V)
    GPIO.setup(
        BLACK_INPUT, GPIO.IN, pull_up_down=GPIO.PUD_UP
    )  # Set BtnPin's mode is input, and pull up to high level(3.3V)
    GPIO.setup(
        RESET, GPIO.IN, pull_up_down=GPIO.PUD_UP
    )  # Set BtnPin's mode is input, and pull up to high level(3.3V)
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
    global team_one, team_two, history
    if team_one.color == "yellow":
        
        history.append("one_score")
        team_one.score += 1

        if (team_one.score >= 5 and team_one.score - team_two.score >= 2) or team_one.score >= 8:
            history.append("one_game")
            game_log.append(Game(team_one.score, team_two.score))
            team_one.score = 0
            team_two.score = 0
            team_one.games += 1
            

    if team_two.color == "yellow":

        history.append("two_score")
        team_two.score += 1

        if (team_two.score >= 5 and team_two.score - team_one.score >= 2) or team_two.score >= 8:
            history.append("two_game")
            game_log.append(Game(team_one.score, team_two.score))
            team_two.score = 0
            team_one.score = 0
            team_two.games += 1


def add_point_black(ev=None):
    global team_one, team_two, history
    if team_one.color == "black":

        history.append("one_score")
        team_one.score += 1

        if (team_one.score >= 5 and team_one.score - team_two.score >= 2) or team_one.score >= 8:
            history.append("one_game")
            game_log.append(Game(team_one.score, team_two.score))
            team_one.score = 0
            team_two.score = 0
            team_one.games += 1

    if team_two.color == "black":

        history.append("two_score")
        team_two.score += 1

        if (team_two.score >= 5 and team_two.score - team_one.score >= 2) or team_two.score >= 8:
            history.append("two_game")
            game_log.append(Game(team_one.score, team_two.score))
            team_two.score = 0
            team_one.score = 0
            team_two.games += 1


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
    global team_one
    global team_two

    if team_one.color == "yellow":

        GPIO.output(YELLOW_GAME_1, team_one.games < 1)
        GPIO.output(YELLOW_GAME_2, team_one.games < 2)
        GPIO.output(YELLOW_GAME_3, team_one.games < 3)
        GPIO.output(BLACK_GAME_1, team_two.games < 1)
        GPIO.output(BLACK_GAME_2, team_two.games < 2)
        GPIO.output(BLACK_GAME_3, team_two.games < 3)

    if team_one.color == "black":

        GPIO.output(YELLOW_GAME_1, team_two.games < 1)
        GPIO.output(YELLOW_GAME_2, team_two.games < 2)
        GPIO.output(YELLOW_GAME_3, team_two.games < 3)
        GPIO.output(BLACK_GAME_1, team_one.games < 1)
        GPIO.output(BLACK_GAME_2, team_one.games < 2)
        GPIO.output(BLACK_GAME_3, team_one.games < 3)


def count_clicks(ev=None):
    global press_count, start_time
    press_count += 1
    start_time = time.time()


def reset():
    global team_one, team_two, game_log, history
    team_one.games = 0
    team_one.score = 0
    team_two.games = 0
    team_two.score = 0
    game_log = []
    history = []


def undo():
    global team_one, team_two, game_log, history
    if len(history) > 0:
        action = history.pop()

        if action is "one_score":
            team_one.score = team_one.score - 1

        if action is "one_game":
            team_one.games = team_one.games - 1
            game: Game = game_log.pop()
            team_one.score = game.team_one_score
            team_two.score = game.team_two_score

        if action is "two_score":
            team_two.score = team_two.score - 1

        if action is "two_game":
            team_two.games = team_two.games - 1
            game: Game = game_log.pop()
            team_one.score = game.team_one_score
            team_two.score = game.team_two_score


def switch_sides():
    global team_one, team_two, history
    team_one.color = "black" if team_one.color == "yellow" else "yellow"
    team_two.color = "black" if team_two.color == "yellow" else "yellow"


def choices():
    global press_count

    # switcher = {1: reset, 2: switch_sides}
    # switcher[press_count]()
    if press_count == 1:
        switch_sides()
    if press_count == 2:
        undo()
    if press_count == 3:
        reset()
    press_count = 0


def render():
    global team_one, team_two
    render_yellow_score(
        segCode[team_one.score if team_one.color == "yellow" else team_two.score]
    )
    render_black_score(
        segCode[team_two.score if team_two.color == "black" else team_one.score]
    )
    render_games()


def loop():
    global start_time, press_count
    GPIO.add_event_detect(YELLOW_INPUT, GPIO.FALLING, callback=add_point_yellow, bouncetime=2000)
    GPIO.add_event_detect(BLACK_INPUT, GPIO.FALLING, callback=add_point_black, bouncetime=2000)
    GPIO.add_event_detect(RESET, GPIO.RISING, callback=count_clicks, bouncetime=200)
    while True:
        if start_time is not None and time.time() - start_time > 0.4:
            start_time = None
            choices()
        else:
            render()
            time.sleep(0.1)  # Don't do anything


def destroy():
    reset()
    GPIO.output(BLACK_GAME_1, GPIO.HIGH)  # led off
    GPIO.output(BLACK_GAME_2, GPIO.HIGH)  # led off
    GPIO.output(BLACK_GAME_3, GPIO.HIGH)  # led off
    GPIO.output(YELLOW_GAME_1, GPIO.HIGH)  # led off
    GPIO.output(YELLOW_GAME_2, GPIO.HIGH)  # led off
    GPIO.output(YELLOW_GAME_3, GPIO.HIGH)  # led off
    GPIO.cleanup()


if __name__ == "__main__":  # Program start from here
    setup()
    reset()
    try:
        loop()
    except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
        destroy()
