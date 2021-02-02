import RPi.GPIO as io
import time
from enum import Enum
import asyncio

class Direction():
    Forward = 1
    Reverse = 2

class Robot():
    def __init__(self):
        io.setwarnings(False) 
        io.cleanup()

        self.FRONT_RIGHT_FORWARD = 6
        self.FRONT_RIGHT_BACKWARD = 5
        self.FRONT_LEFT_FORWARD = 27
        self.FRONT_LEFT_BACKWARD = 17
        self.BACK_RIGHT_FORWARD = 23
        self.BACK_RIGHT_BACKWARD = 24
        self.BACK_LEFT_FORWARD = 26
        self.BACK_LEFT_BACKWARD = 16
        self.FRONT_ENA = 13
        self.FRONT_ENB = 12
        self.BACK_ENA = 19
        self.BACK_ENB = 18

        io.setmode(io.BCM)
        io.setup(self.BACK_RIGHT_FORWARD, io.OUT)
        io.setup(self.BACK_RIGHT_BACKWARD, io.OUT)
        io.setup(self.BACK_LEFT_FORWARD, io.OUT)
        io.setup(self.BACK_LEFT_BACKWARD, io.OUT)
        io.setup(self.FRONT_RIGHT_FORWARD, io.OUT)
        io.setup(self.FRONT_RIGHT_BACKWARD, io.OUT)
        io.setup(self.FRONT_LEFT_FORWARD, io.OUT)
        io.setup(self.FRONT_LEFT_BACKWARD, io.OUT)

        io.output(self.BACK_RIGHT_FORWARD, False)
        io.output(self.BACK_RIGHT_BACKWARD, False)
        io.output(self.BACK_LEFT_FORWARD, False)
        io.output(self.BACK_LEFT_BACKWARD, False)
        io.output(self.FRONT_RIGHT_FORWARD, False)
        io.output(self.FRONT_RIGHT_BACKWARD, False)
        io.output(self.FRONT_LEFT_FORWARD, False)
        io.output(self.FRONT_LEFT_BACKWARD, False)

        io.setup(self.FRONT_ENA, io.OUT)
        io.setup(self.FRONT_ENB, io.OUT)
        io.setup(self.BACK_ENA, io.OUT)
        io.setup(self.BACK_ENB, io.OUT)

        self.front_right_pwm = io.PWM(self.FRONT_ENA, 100)
        self.front_left_pwm = io.PWM(self.FRONT_ENB, 100)
        self.back_right_pwm = io.PWM(self.BACK_ENA, 100)
        self.back_left_pwm = io.PWM(self.BACK_ENB, 100)

        self.front_left_pwm.start(0)
        self.front_left_pwm.ChangeDutyCycle(0)
        self.front_right_pwm.start(0)
        self.front_right_pwm.ChangeDutyCycle(0)
        self.back_left_pwm.start(0)
        self.back_left_pwm.ChangeDutyCycle(0)
        self.back_right_pwm.start(0)
        self.back_right_pwm.ChangeDutyCycle(0)

    def front_left(self, direction: Direction, power: int):
        if direction == Direction.Forward:
            io.output(self.FRONT_LEFT_FORWARD, True)
            io.output(self.FRONT_LEFT_BACKWARD, False)
        else:
            io.output(self.FRONT_LEFT_FORWARD, False)
            io.output(self.FRONT_LEFT_BACKWARD, True)
        self.front_left_pwm.ChangeDutyCycle(power)

    def front_right(self, direction: Direction, power: int):
        if direction == Direction.Forward:
            io.output(self.FRONT_RIGHT_FORWARD, True)
            io.output(self.FRONT_RIGHT_BACKWARD, False)
        else:
            io.output(self.FRONT_RIGHT_FORWARD, False)
            io.output(self.FRONT_RIGHT_BACKWARD, True)
        self.front_right_pwm.ChangeDutyCycle(power)

    def back_left(self, direction: Direction, power: int):
        if direction == Direction.Forward:
            io.output(self.BACK_LEFT_FORWARD, True)
            io.output(self.BACK_LEFT_BACKWARD, False)
        else:
            io.output(self.BACK_LEFT_FORWARD, False)
            io.output(self.BACK_LEFT_BACKWARD, True)
        self.back_left_pwm.ChangeDutyCycle(power)

    def back_right(self, direction: Direction, power: int):
        if direction == Direction.Forward:
            io.output(self.BACK_RIGHT_FORWARD, True)
            io.output(self.BACK_RIGHT_BACKWARD, False)
        else:
            io.output(self.BACK_RIGHT_FORWARD, False)
            io.output(self.BACK_RIGHT_BACKWARD, True)
        self.back_right_pwm.ChangeDutyCycle(power)

    def set_left(self, power:int):
        direction = Direction.Forward
        if power < 0:
            direction = Direction.Reverse
        power = abs(power)
        self.front_left(direction, power)
        self.back_left(direction, power)

    def set_right(self, power:int):
        direction = Direction.Forward
        if power < 0:
            direction = Direction.Reverse
        power = abs(power)
        self.front_right(direction, power)
        self.back_right(direction, power)


    def stop(self):
        io.cleanup()