import pygame as pg
from setting import *
from squre import Squre
from piece import Piece

class Board():

    def __init__(self):

        self.board = self.new_board()

    def new_board(self):

        """
        create a new board
        :return: The board to be ues in the init
        """

        # initialize the board squres (black or white)

        board = [[None] * 8 for i in range(8)]  # The list, on this list we'll make the whole game.


        for x in range(8):
            for y in range(8):
                if (x % 2 != 0) and (y % 2 == 0):
                    board[x][y] = Squre(WHITE, self.squreLocation(x, y))
                elif (x % 2 == 0) and (y % 2 != 0):
                    board[x][y] = Squre(WHITE, self.squreLocation(x, y))
                elif (x % 2 != 0) and (y % 2 != 0):
                    board[x][y] = Squre(BLACK, self.squreLocation(x, y))
                elif (x % 2 == 0) and (y % 2 == 0):
                    board[x][y] = Squre(BLACK, (int(WIDTH / 8 * x + 50), int(HEIGHT / 8 * y + 50)))

        print(board)
        print(board[1][0].pos)

        return board


    def drawBoardGame(self, screen, board):

        """ Draw the all board on the screen """

        for y in range(8):
            for x in range(8):
                pg.draw.rect(screen, self.board[x][y].color, (WIDTH / 8 * x, HEIGHT / 8 * y, WIDTH / 8, HEIGHT / 8), 0)


    def drawAllPieces(self):

        for y in range(8):
            for x in range(8):

                # Draw the all init pieces on the board.  -->> put it in the update section.

                if (x % 2 != 0) and (y % 2 != 0) and (y < 3 or y > 4):
                    if y < 3:
                        self.board[x][y].pieceOn = Piece(GREEN)
                    elif y > 4:
                        self.board[x][y].pieceOn = Piece(RED)
                elif (x % 2 == 0) and (y % 2 == 0) and (y < 3 or y > 4):
                    if y < 3:
                        self.board[x][y].pieceOn = Piece(GREEN)
                    elif y > 4:
                        self.board[x][y].pieceOn = Piece(RED)

    def squreLocation(self, x, y):

        """ Get the squre location.  Argumentes: x, y of the location(min(0,0), max(7,7)).
            Return: tupple of the location """

        return (int(WIDTH / 8 * x + 50), int(HEIGHT / 8 * y + 50))

    def recoSqure(self, mx, my):  # reco == recognizeSqure

        """ Get the mouse position (x, y), does the opposite from squreLocation.
            Return: tupple of the location"""

        print ((int(mx / (WIDTH / 8)), int(my / (HEIGHT / 8)))) # print to ensure it's work

        return (int(mx / (WIDTH / 8)), int(my / (HEIGHT / 8)))

    def inRangeOfBoard(self, pos):

        """ Take a position and Return True if that pos is in the range of the board. """

        x, y = pos
        try:
            if (x < 0) or (y < 0):
                print("BADD")
                return False
            elif self.board[x][y]:
                print("GOOD")
                return True
        except IndexError:
            print("BADD")
            return False

    def listOfMove(self, pos, color):

        """ Return a dictionary of moves the piece can move."""

        x1, y1 = pos
        oldPiecePos = self.board[x1][y1].pieceOn
        d = {}
        whatToRemove = []

        if color == RED: # and oldPiecePos.color == RED:

            d['moveL'] = (x1 - 1, y1 - 1)
            d['moveR'] = (x1 + 1, y1 - 1)
            d['eatL'] = (x1 - 2, y1 - 2), (x1 - 1, y1 - 1)
            d['eatR'] = (x1 + 2, y1 - 2), (x1 + 1, y1 - 1)

        elif color == GREEN: # and oldPiecePos.color == GREEN:

            d['moveL'] = (x1 + 1, y1 + 1)
            d['moveR'] = (x1 - 1, y1 + 1)
            d['eatL'] = (x1 - 2, y1 + 2), (x1 - 1, y1 + 1)
            d['eatR'] = (x1 + 2, y1 + 2), (x1 + 1, y1 + 1)

        for move in d:
            if ('move' in move) and (not self.inRangeOfBoard(d[move])):
                whatToRemove.append(move)
            if ('eat' in move) and (not self.inRangeOfBoard(d[move][0])):
                whatToRemove.append(move)

        for r in whatToRemove:
            del d[r]

        return d

