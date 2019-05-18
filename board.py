import pygame as pg
from setting import *

class Board():

    def __init__(self):

        self.board = self.new_board()

    def new_board(self):

        """
        create a new board
        :return: The board to be ues in the init
        """

        # initialize the board squres (black or white)

        board = [[None] * 8 for i in range(8)]