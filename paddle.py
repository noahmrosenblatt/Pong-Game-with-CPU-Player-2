"""Paddle Class File

Contains Paddle class
"""

from turtle import Turtle


class Paddle(Turtle):
    """A class to represent the paddle owned by a specific Player object, as a subclass of turtle

    Specifies size, shape, and position for paddle.

    Adds methods for drawing paddle, resetting paddle to the center
    and determining directional influence to be applied to ball
    """

    def __init__(self, player_number, paddle_length, screen_width):
        """
        param player_number: The number of the player who owns this Paddle object
        param paddle_length: The length of the paddle (in units for turtlesize() scaling method)
        param screen_width: The width of the screen the paddle operates in
        """
        super().__init__()
        self.player_number = player_number
        self.paddle_length = paddle_length
        self.draw_paddle(self.paddle_length, screen_width)

    def draw_paddle(self, paddle_length, screen_width):
        """
        Draws paddle for start of game, and rotates to correct orientation
        :param paddle_length: The length of the paddle (in units for turtlesize() scaling method)
        :param screen_width: The width of the screen the paddle operates in
                (for determining starting x position for paddle)
        """
        self.color("white")
        self.shape("square")
        self.turtlesize(0.5, paddle_length)
        self.left(90)
        self.penup()
        self.reset_paddle(screen_width)

    def reset_paddle(self, screen_width):
        """
        Resets paddle position after each point is scored
        :param screen_width: The width of the screen the paddle operates in
                (for determining starting x position for paddle)
        """
        if self.player_number == 1:
            self.goto(-screen_width / 2 + 30, 0)
        if self.player_number == 2:
            self.goto(screen_width / 2 - 30, 0)

    def directional_influence(self, ball_y_cor):
        """
        Determines directional influence from paddle to ball depending on distance ball hits from center of paddle.

        Directional influence determines the angle for the ball to be deflected in.
        :param ball_y_cor: y position of center of ball when it hits the paddle
        :return di: A float between -0.8 and 0.8 that provides a linear mapping for angle to deflect ball
                based on paddle's position relative to the ball
        """
        distance_from_center = ball_y_cor - self.ycor()
        # Linear calculation of di for distance of ball from center over half the paddle length
        # Multiplied by 0.8 just to make it so that hitting right at the edge of paddle doesn't
        # make it too close to vertical, where it would take forever to reach the other side
        di = distance_from_center*0.8/(self.paddle_length*10)
        return di
