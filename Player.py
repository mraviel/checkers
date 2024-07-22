

class Player:
    """ Player class.
        Args: pieces_color (str) --> which pieces color is the player color
              my_turn (bool) --> Is it my turn?
              Player (str) optional to add player name """

    def __init__(self, player_number, pieces_color, my_turn, player_name=''):

        self.player_number = player_number  # player number (1 is for bottom pieces and 2 for top pieces)
        self.pieces_color = pieces_color
        self.my_turn = my_turn
        self.player_name = player_name

    def __repr__(self):
        return "{" + f"Player({self.player_number}, {self.pieces_color}, {self.my_turn}, {self.player_name}" + "}"
