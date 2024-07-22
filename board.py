import pygame as pg
from Player import Player
from Settings import *
from Square import Square
from Piece import Piece
import functools



def king_moves(list_of_moves):
    print("\n\n")
    print(list_of_moves)

    if 'move' not in list_of_moves:
        return
    
def get_direction(pos1, pos2):
    
    x_value = pos1[0] - pos2[0]
    y_value = pos1[1] - pos2[1]

    print(f"x_value: {x_value} , y_value: {y_value}")
    return x_value, y_value


def a(l, pos1):
    for pos2 in l:
        get_direction(pos1, pos2)

def check_king_have_piece_on_way(board, current_pos, list_of_moves):

    delete_right_forward, delete_left_forward, delete_right_back, delete_left_back = False, False, False, False
    x, y = current_pos
    new_list = []
    for r in range(0, 8, 1):
        new_move_right_forward = (x - r, y - r)
        new_move_left_forward = (x + r, y - r)
        new_move_right_back = (x + r, y + r)
        new_move_left_back = (x - r, y + r)


        if new_move_right_forward in list_of_moves:
            if board[new_move_right_forward[0]][new_move_right_forward[1]].piece_on:
                delete_right_forward = True
            
            if not delete_right_forward:
                new_list.append(new_move_right_forward)

        if new_move_left_forward in list_of_moves:
            if board[new_move_left_forward[0]][new_move_left_forward[1]].piece_on:
                delete_left_forward = True
            
            if not delete_left_forward:
                new_list.append(new_move_left_forward)
        
        if new_move_right_back in list_of_moves:
            if board[new_move_right_back[0]][new_move_right_back[1]].piece_on:
                delete_right_back = True
            
            if not delete_right_back:
                new_list.append(new_move_right_back)

        if new_move_left_back in list_of_moves:
            if board[new_move_left_back[0]][new_move_left_back[1]].piece_on:
                delete_left_back = True
            
            if not delete_left_back:
                new_list.append(new_move_left_back)

    return new_list
        




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

        x, y = piece.pos
        player = piece.player
        is_king = piece.is_king

        if is_king is False:
            if player.player_number == 1:  # bottom pieces
                list_of_moves['move'] = [(x - 1, y - 1), (x + 1, y - 1)]
                # [[move_pos, eaten_pos], [..., ...]]
                list_of_moves['eat'] = [[(x + 2, y - 2), (x + 1, y - 1)], [(x - 2, y - 2), (x - 1, y - 1)]]

            elif player.player_number == 2:  # top pieces
                list_of_moves['move'] = [(x + 1, y + 1), (x - 1, y + 1)]
                # [[move_pos, eaten_pos], [..., ...]]
                list_of_moves['eat'] = [[(x - 2, y + 2), (x - 1, y + 1)], [(x + 2, y + 2), (x + 1, y + 1)]]

            # make sure move and eat not out of board, move only to Square with no piece on it
            list_of_moves['move'] = [pos for pos in list_of_moves['move'] if
                                     (0 <= pos[0] <= 7 and 0 <= pos[1] <= 7) and
                                     self.board[pos[0]][pos[1]].piece_on is None]

            # make sure move and eat not out of board, for eat if there is move at all and there is a piece to eat
            list_of_moves['eat'] = [move for move in list_of_moves['eat'] if (len(move) == 2)
                                    and (0 <= move[0][0] <= 7 and 0 <= move[0][1] <= 7)
                                    and (0 <= move[1][0] <= 7 and 0 <= move[1][1] <= 7)
                                    and self.board[move[1][0]][move[1][1]].piece_on is not None
                                    and self.board[move[1][0]][move[1][1]].piece_on.player == opposite_player
                                    and self.board[move[0][0]][move[0][1]].piece_on is None]

        # King
        else:
            print('KINGGG')
            list_of_moves = {'move': [], 'eat': [[]]}

            # player 1 and 2 king can do the same moves
            for r in range(0, 8, 1):
                new_move_right_forward = (x - r, y - r)
                new_move_left_forward = (x + r, y - r)
                new_move_right_back = (x + r, y + r)
                new_move_left_back = (x - r, y + r)
                list_of_moves['move'].append(new_move_right_forward)
                list_of_moves['move'].append(new_move_left_forward)
                list_of_moves['move'].append(new_move_right_back)
                list_of_moves['move'].append(new_move_left_back)

            print(f'{list_of_moves} !!')
            # make sure move and eat not out of board, move only to Square with no piece on it
            list_of_moves['move'] = [pos for pos in list_of_moves['move'] if
                                     (0 <= pos[0] <= 7 and 0 <= pos[1] <= 7) and
                                     self.board[pos[0]][pos[1]].piece_on is None]
            
            a(list_of_moves['move'], piece.pos)
            king_moves(list_of_moves)
            print(f"aaa: {check_king_have_piece_on_way(self.board, piece.pos, list_of_moves['move'])}")

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

    def eatPiece(self, from_square, to_square, middle_square):

        """ Make the eat move: move the piece and remove the next position. """

        self.movePiece(from_square, to_square)
        x, y = middle_square.board_pos
        self.board[x][y].piece_on = None

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

    # def listOfMoves(self, pos, color):
    #     """ Return a dictionary of moves the piece can move."""
    #
    #     x1, y1 = pos
    #     oldPiecePos = self.board[x1][y1].piece_on
    #     d = {}
    #
    #     # Add all the legal moves to dict
    #     if (color == RED) and (oldPiecePos is not None) and (oldPiecePos.color == RED):
    #
    #         d['moveL'] = (x1 - 1, y1 - 1)
    #         d['moveR'] = (x1 + 1, y1 - 1)
    #         d['eatL'] = (x1 - 2, y1 - 2), (x1 - 1, y1 - 1)
    #         d['eatR'] = (x1 + 2, y1 - 2), (x1 + 1, y1 - 1)
    #
    #     elif (color == GREEN) and (oldPiecePos is not None) and (oldPiecePos.color == GREEN):
    #
    #         d['moveL'] = (x1 + 1, y1 + 1)
    #         d['moveR'] = (x1 - 1, y1 + 1)
    #         d['eatL'] = (x1 - 2, y1 + 2), (x1 - 1, y1 + 1)
    #         d['eatR'] = (x1 + 2, y1 + 2), (x1 + 1, y1 + 1)
    #
    #     # Delete a pos that is out of range
    #     whatToRemove = []
    #     for move in d:
    #         if ('move' in move) and (not self.inRangeOfBoard(d[move])):
    #             whatToRemove.append(move)
    #         if ('eat' in move) and (not self.inRangeOfBoard(d[move][0])):
    #             whatToRemove.append(move)
    #
    #     for r in whatToRemove:
    #         del d[r]
    #
    #     # Delete a pos that is taken by another piece
    #     whatToRemove = []
    #     for move in d:
    #         if ('move' in move) and (self.posOnBoard(d[move]).piece_on is not None):
    #             whatToRemove.append(move)
    #         if ('eat' in move) and (self.posOnBoard(d[move][0]).piece_on is not None):
    #             whatToRemove.append(move)
    #         if ('eat' in move) and (self.posOnBoard(d[move][1]).piece_on is None):
    #             whatToRemove.append(move)
    #         try:
    #             if ('eat' in move) and (self.posOnBoard(d[move][1]).piece_on.color == color):
    #                 whatToRemove.append(move)
    #         except AttributeError:
    #             pass
    #
    #     for r in whatToRemove:
    #         try:
    #             del d[r]
    #         except KeyError:
    #             print("KEY ERROR")
    #             continue
    #
    #     return d
