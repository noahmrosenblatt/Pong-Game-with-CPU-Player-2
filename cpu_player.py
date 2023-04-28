"""CPU Player Class File

Contains CPU player class
"""

from player import Player
import random


class CPU(Player):
    """A class to represent the CPU player, as a subclass of Player

    Adds additional attributes and methods for reacting to ball
    """

    def __init__(self, paddle_length, paddle_speed, screen_width, screen_height, player_number=2, player_name="CPU"):
        """
        param paddle_length: The length of the paddle to be owned by the player
        param paddle_speed: The speed of the paddle to be owned by the player
        param screen_width: The width of the screen the player operates in
        param screen_height: The height of the screen the plyer operates in
        param player_number: The number of the player being created (defaults to 2 for CPU)
        param player_name: The name of the player (defaults to "CPU" for CPU)
        """
        super().__init__(player_number, paddle_length, paddle_speed, screen_width, screen_height, player_name)
        self.screen_width = screen_width
        self.reacted = False
        # Setting react_x to screen_width to start ensures ball will never cross react_x before reaction
        self.react_x = self.screen_width
        self.di_intent = 0
        self.future_y = None
        self.stop_moving = False

    def set_react_x(self, ball_reset=False):
        """
        Finds x position on screen where CPU reacts after ball hits Player 1's paddle
        (or ball starts by moving to CPU's paddle)
        :param ball_reset: True if ball on reset starts by moving towards CPU's paddle
                (because might be out of range for normal reaction)
        """
        # x position where CPU reacts after ball hits Player 1's paddle
        if ball_reset:
            self.react_x = 0
            self.stop_moving = False
        else:
            self.react_x = random.randint(-self.screen_width/8, self.screen_width/8) + 50
        self.reacted = False

    def react(self, future_y):
        """
        Makes calculated future_y be an attribute of the CPU object to use for
        moving towards where ball will be

        Stops CPU from reacting again until needed

        Determines where CPU's paddle should aim to be, given an offset from ball center
        to apply direction influence (di)
        :param future_y: The y value on the screen where the current ball will be
                once it reaches the CPU's paddle
        """
        self.future_y = future_y
        self.reacted = True
        self.stop_moving = False
        self.react_x = self.screen_width
        # di_intent makes it so that CPU doesn't always aim to hit exactly in the center of the paddle
        self.di_intent = random.uniform(-self.paddle.paddle_length*10, self.paddle.paddle_length*10)
