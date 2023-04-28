"""Player Class File

Contains Player class
"""

from paddle import Paddle


class Player:
    """A class to represent each player"""

    def __init__(self, player_number, paddle_length, paddle_speed, screen_width, screen_height, player_name):
        """
        param player_number: The number of the player being created (1 or 2)
        param paddle_length: The length of the paddle to be owned by the player
        param paddle_speed: The speed of the paddle to be owned by the player
        param screen_width: The width of the screen the player operates in
        param screen_height: The height of the screen the plyer operates in
        param player_name: The name of the player
        """
        self.player_number = player_number
        self.player_name = player_name
        self.paddle_speed = paddle_speed
        self.score = 0
        self.screen_height = screen_height
        self.paddle = Paddle(self.player_number, paddle_length, screen_width)

    def move_paddle_up(self):
        """
        Move paddle up by paddle speed (in pixels)
        """
        if self.paddle.paddle_length*10 < self.screen_height/2 - self.paddle.pos()[1]:
            self.paddle.forward(self.paddle_speed)

    def move_paddle_down(self):
        """
        Move paddle down by paddle speed (in pixels)
        """
        if self.paddle.paddle_length*10 < self.screen_height/2 + self.paddle.pos()[1]:
            self.paddle.backward(self.paddle_speed)
