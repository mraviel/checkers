import pygame as pg
from Settings import *
from os import path
from Board import Board
from Piece import Piece
from Square import Square
from Player import Player
from Client import Client
from Settings import PORT
from datetime import datetime

# location of the img folder
img_dir = path.join(path.dirname(__file__), 'images')
sound_dir = path.join(path.dirname(__file__), 'sound')


class Game:

    def __init__(self):
        # initialize game window, etc
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.running = True  # Game is running?

        self.myBoard = Board()
        self.player1 = Player(player_number=1, pieces_color=RED, my_turn=True, player_name='aviel')
        self.player2 = Player(player_number=2, pieces_color=GREEN, my_turn=False, player_name='chen')
        self.myBoard.initializeBoard(player1=self.player1, player2=self.player2)

        self.prev_moves = {'move': [], 'eat': [[]]}
        self.clicks = []

        self.turn = True
        self.multi = False  # refer to multiple eat
        self.mx, self.my = 0, 0  # pixel location on the screen
        self.end_player_move = False  # player move status (is move ended?)

        # self.client = Client('127.0.0.1', PORT)

    def new(self):
        # start a new game
        self.run()

    def run(self):
        # Game loop
        while self.running:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def update(self):
        # Game loop - update
        # print(datetime.strftime(datetime.now(), "%m:%S.%f"))
        # try:
        #     self.myBoard = self.client.get_board()
        #     print("good")
        # except:
        #     pass
        pass

    def whoPlaying(self):
        # who is playing now?
        if self.player1.my_turn is True:
            main_player = self.player1
            opposite_player = self.player2
        else:
            main_player = self.player2
            opposite_player = self.player1

        return {'main_player': main_player, 'opposite_player': opposite_player}

    def makeMove(self, current_square, prev_square, main_player, opposite_player):
        """ makeMove refer to player how's picked a piece and now want to make a move"""
        current_piece = current_square.pieceSquare()

        status = {}
        # click on place with not piece
        if current_piece is None:
            # if click on piece on first and click on valid move on the second try (move)
            move_list = self.prev_moves['move']
            eat_list = self.prev_moves['eat']

            if self.multi is False and current_square.board_pos in move_list:
                move = self.myBoard.movePiece(prev_square, current_square)
                self.clicks = []
                status['move'] = 'Done'

            # want to eat piece
            elif eat_list:
                for eat in eat_list:
                    if not eat:
                        continue
                    print(f'eat: {eat}')
                    move_to_pos = eat[0]  # 0 always the move to pos
                    eat_pos = eat[1]  # 1 always eat pos
                    eat_square = self.myBoard.posOnBoard(eat_pos)  # eat square in the middle
                    if current_square.board_pos == move_to_pos and \
                            eat_square.piece_on is not None and \
                            eat_square.piece_on.player == opposite_player:
                        self.myBoard.eatPiece(prev_square, current_square, eat_square)

                        list_of_eat = self.myBoard.listOfMoves(current_square.piece_on, main_player, opposite_player, self.multi)['eat']
                        if list_of_eat:
                            self.multi = True   # multiple eat
                            status['eat'] = 'Continue'
                        else:
                            status['eat'] = 'Done'
                            self.multi = False

        if len(self.clicks) == 1 and self.multi is True:
            self.clicks = [self.clicks[0]]
        else:
            self.clicks = []

        # if made a move than see if the piece has become king
        if 'eat' in status and (status['eat'] == 'Done' or status['eat'] == 'Continue') or 'move' in status and (status['move'] == 'Done'):
            if current_square.piece_on.pos[1] == 0 and main_player.player_number == 1:
                current_square.piece_on.is_king = True
            elif current_square.piece_on.pos[1] == 7 and main_player.player_number == 2:
                current_square.piece_on.is_king = True

        return status

    def playerTurn(self, players, end_player_move, x, y):
        """ The turn of the game """

        self.myBoard.squareOrigColor()  # default colors
        status = {}

        main_player = players['main_player']
        opposite_player = players['opposite_player']

        print(f"Player {main_player.player_number} Turn")

        current_square = self.myBoard.board[x][y]
        current_piece = current_square.pieceSquare()
        list_of_moves = self.myBoard.listOfMoves(current_piece, main_player, opposite_player, self.multi)
        current_square.color = BLUE
        if not self.multi:
            self.myBoard.colorPossibleMoves(list_of_moves)  # change colors of possible moves

        print(f'{list_of_moves}: list_of_moves')

        # have prev click
        if len(self.clicks) == 1:

            prev_square = self.myBoard.posOnBoard(self.clicks[0].pos)
            status = self.makeMove(current_square, prev_square, main_player, opposite_player)
            if status == {'eat': 'Continue'}:
                self.multi = True

            if status and self.multi is False:
                self.clicks = []
                end_player_move = True

        # no prev click
        elif len(self.clicks) == 0:

            # if clicks on piece on the first try than add to clicks
            if current_piece is not None:
                self.clicks.append(current_piece)

        # len of clicks is other than 0 or 1
        elif self.multi:
            self.clicks = self.clicks[1]

        else:
            self.clicks = []

        # if multi than save prev_moves as the first click of the multi last turn.
        if not self.multi:
            self.prev_moves = list_of_moves
        else:
            current_piece = self.clicks[0]
            self.prev_moves = self.myBoard.listOfMoves(current_piece, main_player, opposite_player, self.multi)
            self.myBoard.colorPossibleMoves(self.prev_moves)

        # in end of player move and no left of multiple eat replace turns
        if end_player_move and self.multi is False:
            main_player.my_turn = False
            opposite_player.my_turn = True

        print(f"self.clicks: {self.clicks}, multi: {self.multi}")
        return status

    def events(self):

        # Game loop - events
        for event in pg.event.get():
            # check for closing window
            if event.type == pg.QUIT:
                self.running = False

            if event.type == pg.MOUSEBUTTONDOWN:
                self.mx, self.my = pg.mouse.get_pos()
                # print(self.mx, self.my)

                players = self.whoPlaying()
                x, y = Square.pixelToSquare(self.mx, self.my)  # recognize the Square you click on. ex: return (0,0)

                status = self.playerTurn(players, self.end_player_move, x, y)

                # send network player turn 
                print(f"STATUS: {status}")
                # print("Sending Board To Server...")
                # self.client.send_board(self.myBoard)

    def draw(self):
        # Game loop - draw
        self.screen.fill((43, 123, 21))

        self.myBoard.drawBoardGame(self.screen)

        # Update the drawing of the pieces on the basis of rather they have a piece or not!
        for x in range(8):
            for y in range(8):
                if self.myBoard.board[x][y].piece_on is not None:
                    pg.draw.circle(self.screen, self.myBoard.board[x][y].piece_on.color, self.myBoard.board[x][y].pos,
                                   SIZE)

        # after drawing everything, flip the display
        pg.display.flip()

    def show_start_screen(self):
        # the start screen
        self.screen.fill((150, 150, 150))
        intro = True
        while intro:

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    quit()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_SPACE:
                        intro = False
                    if event.key == pg.K_q:
                        pg.quit()
                        quit()

            self.draw_text(text='Checkers', size=50, color=(0, 0, 0), x=WIDTH / 2, y=HEIGHT / 7)
            self.create_button("Aviel", (0,0,0), (255,255,255), (WIDTH, 50), (WIDTH / 2, HEIGHT / 3))
            pg.display.update()
            self.clock.tick(FPS)

    def show_go_screen(self):
        # the game-over screen
        pass

    def draw_text(self, text, size, color, x, y):
        font_name = pg.font.match_font(FONT_NAME)
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)
    
    def create_button(self, text: str, font_color: tuple, bg_color: tuple, size: tuple, pos: tuple):
        """ Create button and return cords (x1, y1, x2, y2) """
        font = pg.font.Font(None, 24)
        button_surface = pg.Surface(size)
        button_surface.fill(bg_color)
        text_obj = font.render(text, True, font_color)
        text_rect = text_obj.get_rect(center=(button_surface.get_width()/2, button_surface.get_height()/2))
        button_rect = pg.Rect(*pos, *size)
        button_surface.blit(text_obj, text_rect)
        self.screen.blit(button_surface, (button_rect.x, button_rect.y))



if __name__ == '__main__':

    # player1 details later to be edited
    player1_color = ''
    player1_name = ''

    # player2 details later to be edited
    player2_color = ''
    player2_name = ''

    g = Game()
    g.show_start_screen()
    while g.running:
        g.new()
        g.show_go_screen()

    pg.quit()
