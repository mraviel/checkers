import pygame as pg
from Player import Player
from Settings import *
from Square import Square
from Piece import Piece



class Board:

    def __init__(self):

        self.board = self.new_board()
        print(self.board)

    @staticmethod
    def new_board():

        """
        create a new board
        :return: The board to be ues in the init
        """

        # initialize the board Squares (black or white)

        board = [[Square(color=RED, pos=(0, 0), board_pos=(0, 0), piece_on=None)] * 8 for i in range(8)]   # Board list, contains all data on the game

        # Squares to board
        for y in range(8):
            for x in range(8):
                if (x % 2 != 0) and (y % 2 == 0):
                    board[x][y] = Square(color=WHITE, pos=Square.SquareToPixel(x, y), board_pos=(x, y))
                elif (x % 2 == 0) and (y % 2 != 0):
                    board[x][y] = Square(color=WHITE, pos=Square.SquareToPixel(x, y), board_pos=(x, y))
                elif (x % 2 != 0) and (y % 2 != 0):
                    board[x][y] = Square(color=BLACK, pos=Square.SquareToPixel(x, y), board_pos=(x, y))
                elif (x % 2 == 0) and (y % 2 == 0):
                    board[x][y] = Square(color=BLACK, pos=Square.SquareToPixel(x, y), board_pos=(x, y))
                    # board[x][y] = Square(BLACK, (int(WIDTH / 8 * x + 50), int(HEIGHT / 8 * y + 50)))

        return board
    
    def getBoardPosition(self, x, y):
        try:
            return self.board[x][y]
        except IndexError:
            return None

    def initializeBoard(self, player1: Player, player2: Player):

        """ Assign Pieces to Squares And Players to pieces """

        for y in range(8):
            for x in range(8):

                # Assign the all start pieces on the board.
                if (x % 2 != 0) and (y % 2 != 0) and (y < 3 or y > 4):
                    if y < 3:
                        self.board[x][y].piece_on = Piece(color=GREEN, pos=self.board[x][y].board_pos, player=player2)
                    elif y > 4:
                        self.board[x][y].piece_on = Piece(color=RED, pos=self.board[x][y].board_pos, player=player1)
                elif (x % 2 == 0) and (y % 2 == 0) and (y < 3 or y > 4):
                    if y < 3:
                        self.board[x][y].piece_on = Piece(color=GREEN, pos=self.board[x][y].board_pos, player=player2)
                    elif y > 4:
                        self.board[x][y].piece_on = Piece(color=RED, pos=self.board[x][y].board_pos, player=player1)

    def drawBoardGame(self, screen):

        """ Draw the all board on the screen """

        for y in range(8):
            for x in range(8):
                pg.draw.rect(screen, self.board[x][y].color, (WIDTH / 8 * x, HEIGHT / 8 * y, WIDTH / 8, HEIGHT / 8), 0)

    def posOnBoard(self, pos):

        """ Take a position (type list / tuple / dict) and put it in the board.
            Return: Squre in (x, y) location."""

        x, y = pos
        return self.board[x][y]

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

    def listOfMoves(self, piece: Piece, main_player: Player, opposite_player: Player, multi: bool):
        """ Get piece list of moves and remove moves that are not valid (ex: move on another piece) +
            Add moves that are valid (ex: eat)
            Get also multi : if there is a multiple eat if true remove all move and keep just the eat options."""

        list_of_moves = {'move': [], 'eat': [[]]}
        if piece is None:
            return list_of_moves
        elif piece.player != main_player:
            return list_of_moves

        list_of_moves['eat'] = piece.piece_eat(board=self.board, opposite_player=opposite_player)
        list_of_moves['move'] = piece.piece_moves(board=self.board)

        # keep just eat
        if multi:
            list_of_moves['move'] = []

        return list_of_moves

    def colorPossibleMoves(self, list_of_moves):
        """ Get list of moves and color them """

        for move in list_of_moves['move']:
            x = move[0]
            y = move[1]
            self.board[x][y].changeColor(YELLOW)

        for eat in list_of_moves['eat']:
            if eat:
                eat_move = eat[0]
                x = eat_move[0]
                y = eat_move[1]
                self.board[x][y].changeColor(YELLOW)

    def squareOrigColor(self):
        """ Change the colors of all squares back to the origin color """

        for y in range(8):
            for x in range(8):
                if (x % 2 != 0) and (y % 2 == 0):
                    self.board[x][y].color = WHITE
                elif (x % 2 == 0) and (y % 2 != 0):
                    self.board[x][y].color = WHITE
                elif (x % 2 != 0) and (y % 2 != 0):
                    self.board[x][y].color = BLACK
                elif (x % 2 == 0) and (y % 2 == 0):
                    self.board[x][y].color = BLACK

    def movePiece(self, from_square, to_square):

        """ Move piece from one position to another """
        print(f"from_square: {from_square}")
        print(f"to_square: {to_square}")

        # move to new location
        x, y = to_square.board_pos
        self.board[x][y].piece_on = from_square.piece_on
        self.board[x][y].piece_on.pos = (x, y)

        # remove old one
        x, y = from_square.board_pos
        self.board[x][y].piece_on = None

        return {'from': from_square, 'to': to_square}

    def eatPiece(self, from_square, to_square, middle_square):

        """ Make the eat move: move the piece and remove the next position. """

        self.movePiece(from_square, to_square)
        x, y = middle_square.board_pos
        self.board[x][y].piece_on = None
        return {'from_squre': from_square, 'to_square': to_square, 'eat_square': middle_square}

    def movePieceTurn(self, oldPos, newPos, canMoves):

        """ The turn of the game each player move in his turn."""

        x1, y1 = oldPos
        x2, y2 = newPos

        print(canMoves)

        # move piece
        for move in canMoves:

            if ('move' in move) and ((x2, y2) == canMoves[move]):
                # make a move
                self.movePiece(oldPos, newPos)
                return "MOVE JUST HAPPEND"

            elif ('eat' in move) and ('R' in move) and ((x2, y2) == canMoves[move][0]) and (x1 - x2 < 0):  # eat to right
                # remove next piece and move the piece
                self.eatPiece(oldPos, newPos, canMoves[move][1])
                return "EAT JUST HAPPEND (RIGHT)"

            elif ('eat' in move) and ('L' in move) and ((x2, y2) == canMoves[move][0]) and (x1 - x2 > 0):  # eat to left
                # remove next piece and move the piece
                self.eatPiece(oldPos, newPos, canMoves[move][1])
                return "EAT JUST HAPPEND (LEFT)"

        return "NOTHING HAPPEND"
