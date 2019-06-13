import pygame as pg
from setting import *
from os import path
from board import Board
from piece import Piece

# location of the img folder
img_dir = path.join(path.dirname(__file__), 'images')
sound_dir = path.join(path.dirname(__file__), 'sound')

class Game:

    def __init__(self):
        # initiallize game window, etc
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.running = True
        self.myBoard = Board()
        self.myBoard.drawAllPieces()
        self.clicks = []


    def new(self):
        # start a new game
        self.run()

    def run(self):
        # Game loop
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def update(self):
        # Game loop - update
        pass

    def events(self):
        # Game loop - events
        for event in pg.event.get():
            # check for closing window
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            if event.type == pg.MOUSEBUTTONDOWN:
                self.mx, self.my = pg.mouse.get_pos()
                print (self.mx, self.my)
                self.myBoard.recoSqure(self.mx, self.my)   # -->> recognize the squre you click on. ex: return (0,0)
                self.clicks.append(self.myBoard.recoSqure(self.mx, self.my))

                # Make a move :)
                if (len(self.clicks) == 2) and (self.clicks[0] != self.clicks[1]):  # -->> If clicks 2 times and in diffrent place.
                    print(self.movePiece(self.clicks[0], self.clicks[1]))

                elif len(self.clicks) == 2 and self.clicks[0] == self.clicks[1]:  # -->> If clicks 2 times and in the same place.
                    self.clicks = [self.clicks[0]]

                elif len(self.clicks) > 2:  # Reset the move.
                    self.clicks = []
                    self.clicks.append(self.myBoard.recoSqure(self.mx, self.my))

                print(self.clicks)


    def draw(self):
        # Game loop - draw
        self.screen.fill((43,123,21))

        self.myBoard.drawBoardGame(self.screen, self.myBoard)


        # self.myBoard.board[0][0].pieceOn = Piece(RED)

        # Update the drawing of the pieces on the basis of rather they have a piece or not!
        for x in range(8):
            for y in range(8):
                if self.myBoard.board[x][y].pieceOn != None:
                    pg.draw.circle(self.screen, self.myBoard.board[x][y].pieceOn.color, self.myBoard.board[x][y].pos, SIZE)


        # after drawing everything, flip the display
        pg.display.flip()

    def show_start_screen(self):
        # the start screen
        pass

    def show_go_screen(self):
        # the game-over screen
        pass


    def draw_text(self, text, size, color, x, y):
        font = pg.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)

    def test(self):

        """ Test if the all the function are working! """

        assert self.myBoard.recoSqure(115, 101) == (1,0)
        assert self.myBoard.recoSqure(192, 790) == (1,7)

        print("All function are work!")


    def movePiece(self, oldPos, newPos):
        x1, y1 = oldPos
        x2, y2 = newPos

        # move piece (red move)
        if ((((x1-1) == x2) and ((y1-1) == y2) or ((x1+1) == x2) and ((y1-1) == y2))) and (self.myBoard.board[x2][y2].pieceOn == None) and \
            (self.myBoard.board[x1][y1].pieceOn != None) and (self.myBoard.board[x1][y1].pieceOn.color == RED):
            self.myBoard.board[x1][y1].pieceOn = None
            self.myBoard.board[x2][y2].pieceOn = Piece(RED)
            return "RED JUST MOVE"

        # move piece (green move)
        elif ((((x1 + 1) == x2) and ((y1 + 1) == y2) or ((x1 - 1) == x2) and ((y1 + 1) == y2))) and (self.myBoard.board[x2][y2].pieceOn == None) and \
             (self.myBoard.board[x1][y1].pieceOn != None) and (self.myBoard.board[x1][y1].pieceOn.color == GREEN):
                self.myBoard.board[x1][y1].pieceOn = None
                self.myBoard.board[x2][y2].pieceOn = Piece(GREEN)
                return "GREEN JUST MOVE"

        # eat a piece (red eat green)
        elif ((self.myBoard.board[x2][y2].pieceOn == None)) and \
             ((x1+2) == x2) and ((y1-2) == y2) and (self.myBoard.board[x1+1][y1-1].pieceOn != None) and (self.myBoard.board[x1+1][y1-1].pieceOn.color == GREEN):
                self.myBoard.board[x1 + 1][y1 - 1].pieceOn = None
                self.myBoard.board[x2][y2].pieceOn = self.myBoard.board[x1][y1].pieceOn # move the piece to another location after the eat
                self.myBoard.board[x1][y1].pieceOn = None # delate the old piece position
                return ("RED EAT THE GREEN")
        elif ((self.myBoard.board[x2][y2].pieceOn == None)) and \
             (((x1-2) == x2) and ((y1-2) == y2) and (self.myBoard.board[x1-1][y1-1].pieceOn != None) and (self.myBoard.board[x1-1][y1-1].pieceOn.color == GREEN)):
                self.myBoard.board[x1 - 1][y1 - 1].pieceOn = None
                self.myBoard.board[x2][y2].pieceOn = self.myBoard.board[x1][y1].pieceOn
                self.myBoard.board[x1][y1].pieceOn = None
                return ("RED EAT THE GREEN")

            # eat a piece (green eat red)
        elif ((self.myBoard.board[x2][y2].pieceOn == None)) and \
             (((x1-2) == x2) and ((y1+2) == y2) and (self.myBoard.board[x1-1][y1+1].pieceOn != None) and  (self.myBoard.board[x1-1][y1+1].pieceOn.color == RED)):
                self.myBoard.board[x1-1][y1+1].pieceOn = None
                self.myBoard.board[x2][y2].pieceOn = self.myBoard.board[x1][y1].pieceOn
                self.myBoard.board[x1][y1].pieceOn = None
                return ("GREEN EAT THE RED")
        elif (((x1+2) == x2) and ((y1+2) == y2) and (self.myBoard.board[x1+1][y1+1].pieceOn != None) and (self.myBoard.board[x1+1][y1+1].pieceOn.color == RED)):
            self.myBoard.board[x1+1][y1+1].pieceOn = None
            self.myBoard.board[x2][y2].pieceOn = self.myBoard.board[x1][y1].pieceOn
            self.myBoard.board[x1][y1].pieceOn = None
            return ("GREEN EAT THE RED")

        else:
            return "NOTHING HAPPEND"



g = Game()
g.test() # test if all function are working!
g.show_start_screen()
while g.running:
    g.new()
    g.show_go_screen()

pg.quit()