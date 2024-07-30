from Square import Square
from Player import Player


class Piece:

    def __init__(self, color, pos: tuple, player: Player, is_king=False, picked=False):

        self.color = color
        self.pos = pos
        self.player = player
        self.is_king = is_king
        self.picked = picked

    def piece_moves(self, board):
        current_x, current_y = self.pos 
        
        print(f"{current_x}, {current_y}")
        moves = []

        move_mapper = {1: [(-1, -1), (1, -1)], 2: [(1, 1), (-1, 1)], 'king': [(-1, -1), (-1, 1), (1, -1), (1, 1)]}  # player1 and player2 or king move mapper.
        directions = move_mapper['king'] if self.is_king else move_mapper[self.player.player_number]

        for dr, dc in directions:
            x, y = current_x + dr, current_y + dc
            print(f"dr: {dr}, dc: {dc}, x: {x}, y: {y}")

            while 0 <= x <= 7 and 0 <= y <= 7:
                    if board[x][y].piece_on is None:
                        moves.append((x, y))
                    else:
                        break
                    
                    if not self.is_king:
                        break

                    x += dr
                    y += dc

        return moves
    
    def piece_eat(self, board, opposite_player):
        current_x, current_y = self.pos 
        
        print(f"{current_x}, {current_y}")
        moves = []

        move_mapper = {1: [(-1, -1), (1, -1)], 2: [(1, 1), (-1, 1)], 'king': [(-1, -1), (-1, 1), (1, -1), (1, 1)]}  # player1 and player2 or king move mapper.
        directions = move_mapper['king'] if self.is_king else move_mapper[self.player.player_number]

        for dr, dc in directions:
            x, y = current_x + dr, current_y + dc
            print(f"dr: {dr}, dc: {dc}, x: {x}, y: {y}")

            while 0 <= x <= 7 and 0 <= y <= 7:
                    if board[x][y].piece_on is not None and board[x][y].piece_on.player == opposite_player:
                        land_x, land_y = x + dr, y + dc
                        if 0 <= land_x <= 7 and 0 <= land_y <= 7 and board[land_x][land_y].piece_on is None:
                            moves.append([(land_x, land_y), (x, y)])
                        else: 
                             break
                    # else:
                    #     break
                    
                    if not self.is_king:
                        break

                    x += dr
                    y += dc 

        return moves

    def __repr__(self):
        return "{" + f"Piece({self.color}, {self.pos}, {self.player}, {self.is_king}, {self.picked}" + "}"
