"""Pong Game Main File

Created by: Noah Rosenblatt

Run this script to start Pong game. Change global constants as desired.

Notable features include an AI Player 2 that reacts to the player's shot
in a human-like imperfect manner, and a paddle that allows for a certain degree
of directional influence on the ball depending on where the ball hits relative
to the center of the paddle.
"""

from turtle import Screen, Turtle
import time
from player import Player
from cpu_player import CPU
from ball import Ball
from text_display import Scoreboard, NameDisplay, FinalDisplay

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 500
SCREEN_TITLE = "PONG"
PADDLE_LENGTH = 5
PADDLE_SPEED = 40
STARTING_BALL_SPEED = 3
WINNING_SCORE = 5


def horizontal_wall_collision(current_ball):
    """
    Checks for ball collision with top and bottom walls
    :param current_ball: The ball being checked for collision
    :return: Boolean that is True if collision detected and False if not
    """
    if SCREEN_HEIGHT/2 - abs(current_ball.pos()[1]) < current_ball.radius:
        return True
    else:
        return False


def vertical_wall_collision(current_ball):
    """
    Checks for ball collision with left and right walls
    :param current_ball: The ball being checked for collision
    :return: Boolean that is True if collision detected and False if not
    """
    if SCREEN_WIDTH/2 - abs(current_ball.pos()[0]) < current_ball.radius:
        if current_ball.left_right() == "left":
            player_2.score += 1
            player_2_scoreboard.clear()
            player_2_scoreboard.rewrite(player_2)
        else:
            player_1.score += 1
            player_1_scoreboard.clear()
            player_1_scoreboard.rewrite(player_1)
        return True
    else:
        return False


def paddle_collision(current_ball):
    """
    Checks for ball collision with each paddle
    :param current_ball: The ball being checked for collision
    :return: 2-entry list:
        First: Boolean that is True if collision detected and False if not
        Second: Player object that owns the paddle that was collided with; None if no collision
    """
    if current_ball.xcor() - current_ball.radius <= player_1.paddle.xcor() + player_1.paddle.turtlesize()[0]*10:
        if current_ball.left_right() == "left":
            paddle_max_y = player_1.paddle.ycor() + player_1.paddle.paddle_length*10
            paddle_min_y = player_1.paddle.ycor() - player_1.paddle.paddle_length*10
            if paddle_min_y <= current_ball.ycor() <= paddle_max_y:
                return [True, player_1]
    elif current_ball.xcor() + current_ball.radius >= player_2.paddle.xcor() - player_2.paddle.turtlesize()[0]*10:
        if current_ball.left_right() == "right":
            paddle_max_y = player_2.paddle.ycor() + player_2.paddle.paddle_length*10
            paddle_min_y = player_2.paddle.ycor() - player_2.paddle.paddle_length*10
            if paddle_min_y <= current_ball.ycor() <= paddle_max_y:
                return [True, player_2]
    return [False, None]


def simulate_ball_path(current_ball):
    """
    Create invisible Ball object that simulates faster version of current ball to determine which y position
    CPU paddle will ultimately need to be in order to get to the ball on time for the next shot
    :param current_ball: The ball to be simulated
    :return: y coordinate of center of ball when the current ball will reach the edge of the paddle in the future
    """
    simulated_ball = Ball(STARTING_BALL_SPEED, current_ball)
    player_2_paddle_left_edge = player_2.paddle.xcor() - player_2.paddle.turtlesize()[0]*10
    while simulated_ball.xcor() + simulated_ball.radius <= player_2_paddle_left_edge:
        simulated_ball.move_ball()
        if horizontal_wall_collision(simulated_ball):
            simulated_ball.deflect('y')
    return simulated_ball.ycor()


# Set up screen
screen = Screen()
screen.setup(width=SCREEN_WIDTH, height=SCREEN_HEIGHT)
screen.title(SCREEN_TITLE)
screen.bgcolor("black")
# Get object movements to be drawn simultaneously
screen.tracer(0)
screen.update()

# Create vertical half-court line
half_court = Turtle()
half_court.hideturtle()
half_court.pencolor("white")
half_court.speed('fastest')
half_court.penup()
half_court.goto(0, SCREEN_HEIGHT/2)
half_court.right(90)
while half_court.pos()[1] > -SCREEN_HEIGHT/2:
    half_court.pendown()
    half_court.forward(10)
    half_court.penup()
    half_court.forward(10)

# Create players, paddles, scoreboard, and ball
player_1_name = screen.textinput("Player Name", "What's your name? ")
player_1 = Player(1, PADDLE_LENGTH, PADDLE_SPEED, SCREEN_WIDTH, SCREEN_HEIGHT, player_1_name)
player_2 = CPU(PADDLE_LENGTH, PADDLE_SPEED/30, SCREEN_WIDTH, SCREEN_HEIGHT)
player_1_scoreboard = Scoreboard(player_1)
player_2_scoreboard = Scoreboard(player_2)
player_1_name_display = NameDisplay(player_1)
player_2_name_display = NameDisplay(player_2)
ball = Ball(STARTING_BALL_SPEED)
# If ball starts moving to the right, CPU needs to react right away without waiting for the ball to come from Player 1
if ball.left_right() == "right":
    player_2.set_react_x(ball_reset=True)
screen.update()

# Play game
while player_1.score < WINNING_SCORE and player_2.score < WINNING_SCORE:
    screen.listen()
    # Player 1 moves
    screen.onkeypress(player_1.move_paddle_up, "w")
    screen.onkeypress(player_1.move_paddle_down, "s")
    # Check for Player 2 reaction
    if ball.xcor() >= player_2.react_x and not player_2.reacted:
        player_2.react(future_y=simulate_ball_path(ball))
    # Player 2 moves towards where ball will be if reacting
    if player_2.reacted and not player_2.stop_moving:
        if player_2.paddle.ycor() < min(player_2.future_y + player_2.di_intent, SCREEN_HEIGHT/2):
            player_2.move_paddle_up()
            if player_2.paddle.ycor() >= min(player_2.future_y + player_2.di_intent, SCREEN_HEIGHT/2):
                player_2.stop_moving = True
        elif player_2.paddle.ycor() > max(player_2.future_y + player_2.di_intent, -SCREEN_HEIGHT/2):
            player_2.move_paddle_down()
            if player_2.paddle.ycor() <= max(player_2.future_y + player_2.di_intent, -SCREEN_HEIGHT/2):
                player_2.stop_moving = True
    # Player 2 moves back towards center if ball moving back towards Player 1
    if ball.left_right() == "left":
        # In case CPU never had to move paddle to meet future ball position
        player_2.stop_moving = True
        # Don't start moving back to center until ball is close to the other player's paddle, and don't continue after
        # hitting Player 1's paddle if Player 2's paddle hasn't reached center yet
        if ball.xcor() <= player_1.paddle.xcor() + 100:
            # Don't move paddle if within half a paddle_speed unit (the amount a move_paddle method moves by)
            # to avoid overshoot
            if player_2.paddle.ycor() < 0 - player_2.paddle_speed/2:
                player_2.move_paddle_up()
            elif player_2.paddle.ycor() > 0 + player_2.paddle_speed/2:
                player_2.move_paddle_down()
    # Ball moves
    ball.move_ball()
    screen.update()
    if horizontal_wall_collision(ball):
        ball.deflect('y')
    # Check if round over
    elif vertical_wall_collision(ball):
        ball.hideturtle()
        screen.update()
        # Reset round
        if player_1.score < WINNING_SCORE and player_2.score < WINNING_SCORE:
            time.sleep(2)
            ball.restart_ball(STARTING_BALL_SPEED)
            ball.showturtle()
            player_1.paddle.reset_paddle(SCREEN_WIDTH)
            player_2.paddle.reset_paddle(SCREEN_WIDTH)
            screen.update()
            # If ball starts moving to the right, CPU needs to react right away without waiting for the ball to come
            # from Player 1
            if ball.left_right() == "right":
                player_2.set_react_x(ball_reset=True)
            time.sleep(2)
    elif paddle_collision(ball)[0]:
        # Determines strength of paddle directional influence
        # (0 if ball hits middle of paddle, 1 if top, and -1 if bottom)
        di = paddle_collision(ball)[1].paddle.directional_influence(ball.ycor())
        if paddle_collision(ball)[1] is player_1:
            player_2.set_react_x()
        ball.deflect('x', di)

# End game by displaying winner
if player_2.score == WINNING_SCORE:
    final_display = FinalDisplay(player_2)
else:
    final_display = FinalDisplay(player_1)


screen.exitonclick()
