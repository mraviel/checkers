

class Squre():

    def __init__(self, color, pos, pieceOn=None):

        self.color = color  # the color of the squre (black or white)
        self.pos = pos
        self.pieceOn = pieceOn  # is there any piece on the squre? -->> have the piece object on it!