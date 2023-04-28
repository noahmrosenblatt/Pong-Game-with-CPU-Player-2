"""Display Information on Screen

Contains separate classes of scoreboard, player names, and text popup showing winner
"""

from turtle import Turtle

# For the lols
FONT = ('Comic Sans MS', 40, 'normal')


def basic_board(board):
    """
    Common parameters for each type of text to display
    :param board: The board containing text to display
    """
    board.color("white")
    board.hideturtle()
    board.penup()


class Scoreboard(Turtle):
    """A class to represent each player's scoreboard"""

    def __init__(self, player):
        """
        param player: The player whose score needs to be displayed
        """
        super().__init__()
        basic_board(self)
        self.rewrite(player)

    def rewrite(self, player):
        """
        Rewrite player's score on screen
        :param player: The player whose score needs to be displayed
        """
        if player.player_number == 1:
            self.goto(-85, player.screen_height/2 - 120)
        else:
            self.goto(85, player.screen_height/2 - 120)
        self.write(arg=player.score, align='center', font=FONT)


class NameDisplay(Turtle):
    """A class to represent each player's name"""

    def __init__(self, player):
        """
        param player: The player whose name needs to be displayed
        """
        super().__init__()
        basic_board(self)
        self.rewrite(player)

    def rewrite(self, player):
        """
        Rewrite player's name on screen
        :param player: The player whose name needs to be displayed
        """
        if player.player_number == 1:
            self.goto(-85, player.screen_height/2 - 60)
        else:
            self.goto(85, player.screen_height/2 - 60)
        self.write(arg=player.player_name, align='center', font=FONT)


class FinalDisplay(Turtle):
    """A class to represent winning player's name"""

    def __init__(self, player):
        """
        param player: The player whose name needs to be displayed with winning message
        """
        super().__init__()
        basic_board(self)
        self.goto(0, 50)
        self.winning_message(player)

    def winning_message(self, player):
        """
        Write winning message with corresponding player on screen
        :param player: The player whose name needs to be displayed with winning message
        """
        winning_text = f"{player.player_name} is the winner"
        self.write(arg=winning_text, align='center', font=FONT)
