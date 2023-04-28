"""Ball Class File

Contains Ball class, as a subclass of Turtle
"""

from turtle import Turtle
import random
import numpy as np


def cart2pol(velocity):
    """
    Convert velocity from cartesian coordinates to polar coordinates
    :param velocity: 2-entry list of velocity given in cartesian coordinates (x-vel, y-vel)
    :return: 2-entry list of velocity given in polar coordinates (speed, angle up from positive x-axis)
    """
    rho = np.sqrt(velocity[0] ** 2 + velocity[1] ** 2)
    phi = np.degrees(np.arctan2(velocity[1], velocity[0]))
    return [rho, phi]


def pol2cart(velocity):
    """
    Convert velocity from polar coordinates to cartesian coordinates
    :param velocity: 2-entry list of velocity given in polar coordinates (speed, angle up from positive x-axis)
    :return: 2-entry list of velocity given in cartesian coordinates (x-vel, y-vel)
    """
    x = velocity[0] * np.cos(np.radians(velocity[1]))
    y = velocity[0] * np.sin(np.radians(velocity[1]))
    return [x, y]


class Ball(Turtle):
    """A class to represent either the actual ball or an invisible ball for simulation"""

    def __init__(self, starting_ball_speed, ball_to_simulate=None):
        """
        param starting_ball_speed: Speed that the ball starts moving at
        param ball_to_simulate: Ball object that will be simulated; defaults to None
        """
        super().__init__()
        self.color("white")
        self.shape("circle")
        self.turtlesize(0.5, 0.5)
        self.penup()
        # Each unit of turtle size is 20 pixels, so radius would be half that
        self.radius = self.turtlesize()[0]*10
        self.velocity = [starting_ball_speed, 0]
        if ball_to_simulate is not None:
            self.ball_to_simulate = ball_to_simulate
            self.start_simulated_ball()
        else:
            self.restart_ball(starting_ball_speed)

    def start_simulated_ball(self):
        """
        Copy parameters from ball-to-simulate to simulating ball
        """
        self.goto(self.ball_to_simulate.pos())
        self.velocity[1] = self.ball_to_simulate.velocity[1]
        self.setheading(self.velocity[1])
        self.hideturtle()

    def restart_ball(self, ball_speed):
        """
        Restarts ball's position and velocity at start of game or new round
        :param ball_speed: Speed that the ball will move at
        """
        self.goto(0, 0)
        # First number is speed; second number is heading
        # Don't start ball going 90 degrees (straight up) or 270 (straight down)
        initial_direction = random.choice([i for i in range(0, 360) if i not in [90, 270]])
        self.velocity = [ball_speed, initial_direction]
        self.setheading(self.velocity[1])

    def move_ball(self):
        """
        Moves ball by speed given by first entry of velocity attribute
        :return:
        """
        self.forward(self.velocity[0])

    def deflect(self, direction, di=None):
        """
        Negates ball speed in given direction ('x' or 'y').

        If deflecting off of paddle, then applies direction influence (di) to ball's deflection angle
        :param direction: 'x' or 'y'
        :param di: directional influence value if hitting paddle
        """
        # Deflect off top or bottom wall
        if direction == 'y':
            cart_velocity = pol2cart(self.velocity)
            cart_velocity[1] = -cart_velocity[1]
            self.velocity = cart2pol(cart_velocity)
            self.setheading(self.velocity[1])
        # Deflect off paddle
        elif direction == 'x':
            # Deflect off left paddle
            if self.left_right() == "left":
                self.velocity[1] = 90*di
            # Deflect off right paddle
            else:
                self.velocity[1] = 180 - 90*di
            self.setheading(self.velocity[1])

    def left_right(self):
        """
        Determines if ball is moving left or right based on ball's heading angle
        :return: str that provides direction ball is moving in
        """
        # Checks self.heading() instead of self.velocity[1] because heading method converts angle to between 0 and 360
        if 90 < self.heading() < 270:
            return "left"
        else:
            return "right"
