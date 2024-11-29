from Core.cell_position import CellPosition
from pieces import Grasshopper, Ant, Beetle, Spider, Queen

class AvailablePieces:
    def __init__(self, player_number):
        self.pieces = [Grasshopper(player_number)] * 3
        self.pieces += [Ant(player_number)] * 3
        self.pieces += [Beetle(player_number)] * 2
        self.pieces += [Spider(player_number)] * 2
        self.pieces += [Queen(player_number)] * 1

    def __str__(self):
        return ", ".join(str(piece) for piece in self.pieces)

    def __repr__(self):
        return "[" + self.__str__() + "]"

    def __iter__(self):
        for piece in self.pieces:
            yield piece

    def update(self, piece):
        if piece in self.pieces:
            return self.pieces.pop(self.pieces.index(piece))
        else:
            raise ValueError(f"{piece} not found in available pieces: {[str(p) for p in self.pieces]}.")

    def is_this_piece_available(self, piece):
        return piece in self.pieces



class Player:
    def __init__(self, player_number,player_type,player_level):
        self.unplaced_pieces = AvailablePieces(player_number)
        self.placed_pieces = {}
        self.player_type = player_type
        self.player_number = player_number
        self.player_level = player_level # e for easy, m for medium, h for hard, p if player
        self.moves_count = 0
        self.player_won = False
        self.queen = None

    def get_level(self):
        return self.player_level

    def get_moves_count(self):
        return self.moves_count

    def get_player_number(self):
        return self.player_number

    def get_queen(self):
        return self.queen

    def queen_unplaced(self):
        return Queen(self.player_number) in self.unplaced_pieces

    def set_queen(self,cell: CellPosition):
        self.queen = cell

    def update_available_pieces(self,piece,cell):
        self.unplaced_pieces.update(piece)
        self.placed_pieces[piece] = cell

    def placed_pieces_has_moves(self, board_state):
        for piece, cell in self.placed_pieces.items():
            available_moves = piece.get_available_moves(cell, board_state)
            if available_moves:
                return True
        return False

