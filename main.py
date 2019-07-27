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
        self.turn = True
        self.multi = False
        self.d = {}

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

                self.d = {}  # Initialize the dict.

                if self.turn is True:
                    canMoves = self.myBoard.listOfMoves(self.clicks[0], RED)
                else:
                    canMoves = self.myBoard.listOfMoves(self.clicks[0], GREEN)

                # Remove part of the dict if it needed. (if there is multiple eat or not)
                if not self.multi:
                    for key, value in canMoves.items():
                        self.d[key] = value
                else:
                    # I will use the var self.multi soon!
                    for key, value in canMoves.items():
                        if 'eat' in key:
                            self.d[key] = value

                # Make a move :)
                isIn = False
                if len(self.clicks) == 2 and self.clicks[0] != self.clicks[1]:
                    if self.turn:
                        print("RED IS PLAY")
                    else:
                        print("GREEN IS PLAY")

                    # Check if the second click is in the dict.
                    for value in self.d.values():
                        if self.clicks[1] == value or self.clicks[1] in value:
                            isIn = True

                    # If isIn make a move
                    if isIn:
                        try:
                            if self.turn and self.myBoard.posOnBoard(self.clicks[0]).pieceOn.color == RED:
                                # Only if red move and the piece is red.
                                move = self.myBoard.movePieceTurn(self.clicks[0], self.clicks[1], self.d)
                            elif not self.turn and self.myBoard.posOnBoard(self.clicks[0]).pieceOn.color == GREEN:
                                # Only if green move and the piece is green.
                                move = self.myBoard.movePieceTurn(self.clicks[0], self.clicks[1], self.d)
                            else:
                                # If not than, this is not your turn! (Try to click again!)
                                move = "Is Not Your Turn"
                                self.clicks = []

                        except AttributeError:
                            move = "Is Not Your Turn"
                            self.clicks = []

                    else:
                        move = "NOT VALID MOVE"
                        self.clicks = []

                    if move != "NOTHING HAPPEND" and move != "NOT VALID MOVE" and move != "Is Not Your Turn":
                        # If was made a move, change the turn.
                        self.turn = not self.turn
                    print(move)

                # -->> If clicks 2 times and in the same place.
                elif len(self.clicks) == 2 and self.clicks[0] == self.clicks[1]:
                    self.clicks = []

                elif len(self.clicks) > 2:  # Reset the move.
                    self.clicks = []
                    self.clicks.append(self.myBoard.recoSqure(self.mx, self.my))

                print(self.clicks)

    def draw(self):
        # Game loop - draw
        self.screen.fill((43, 123, 21))

        self.myBoard.drawBoardGame(self.screen, self.myBoard)

        # Update the drawing of the pieces on the basis of rather they have a piece or not!
        for x in range(8):
            for y in range(8):
                if self.myBoard.board[x][y].pieceOn is not None:
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
        font = pg.font.Font(FONT_NAME, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)

    def test(self):

        """ Test if the all the function are working! """

        assert self.myBoard.recoSqure(115, 101) == (1, 0)
        assert self.myBoard.recoSqure(192, 790) == (1, 7)

        print("All function are work!")


g = Game()
g.test()  # test if all function are working!
g.show_start_screen()
while g.running:
    g.new()
    g.show_go_screen()

pg.quit()
