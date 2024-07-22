from Square import Square
from Player import Player


class Piece:

    def __init__(self, color, pos: tuple, player: Player, is_king=False, picked=False):

        self.color = color
        self.pos = pos
        self.player = player
        self.is_king = is_king
        self.picked = picked

    def __repr__(self):
        return "{" + f"Piece({self.color}, {self.pos}, {self.player}, {self.is_king}, {self.picked}" + "}"