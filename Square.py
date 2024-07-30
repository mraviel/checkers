from Settings import *
# from Piece import Piece


class Square:

    def __init__(self, color: tuple, pos: tuple, board_pos: tuple, piece_on=None):

        self.color = color  # the color of the Square (black or white)
        self.pos = pos  # pos by pixels
        self.piece_on = piece_on  # is there any piece on the Square? -->> have the piece object on it!
        self.board_pos = board_pos

    @staticmethod
    def SquareToPixel(x, y):
        """ Get the squre location.  Arguments: x, y of the location(min(0,0), max(7,7)).
            Return: tuple of the pixel location (x, y) """

        return int(WIDTH / 8 * x + 50), int(HEIGHT / 8 * y + 50)

    @staticmethod
    def pixelToSquare(mx, my):  # calculate pixels to square tuple

        """ Get the mouse position (x, y), does the opposite from SquareToPixel.
            Return: tuple of the location"""

        # print(int(mx / (WIDTH / 8)), int(my / (HEIGHT / 8)))  # print to ensure it's work

        return int(mx / (WIDTH / 8)), int(my / (HEIGHT / 8))

    def pieceSquare(self) -> object:
        """ Return piece on square """
        # print(self.piece_on)
        return self.piece_on

    def changeColor(self, color):
        """ Change color of square """
        self.color = color


    def __repr__(self):
        return "{" + f"Square({self.color}, {self.board_pos}, {self.piece_on}" + "}"
