from Core.cell_position import CellPosition
from pieces import Grasshopper, Ant, Beetle, Spider, Queen
import copy
class AvailablePieces:
    def __deepcopy__(self, memo):
        # Create a new instance
        new_copy = AvailablePieces(self.pieces[0].player if self.pieces else None)

        # Deepcopy the pieces list
        new_copy.pieces = copy.deepcopy(self.pieces, memo)

        return new_copy

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
    def add_back(self, piece):
        return self.pieces.append(piece)

    def is_this_piece_available(self, piece):
        return piece in self.pieces



class Player:

    def __deepcopy__(self, memo):
        # Create a new instance
        new_copy = Player(self.player_number, self.player_type, self.player_level)

        # Deepcopy mutable attributes
        new_copy.unplaced_pieces = copy.deepcopy(self.unplaced_pieces, memo)
        new_copy.placed_pieces = copy.deepcopy(self.placed_pieces, memo)
        new_copy.moves_count = self.moves_count
        new_copy.player_won = self.player_won
        new_copy.queen = copy.deepcopy(self.queen, memo) if self.queen else None

        return new_copy
    def __init__(self, player_number,player_type,player_level):
        self.unplaced_pieces = AvailablePieces(player_number)
        self.placed_pieces = list()
        self.player_type = player_type
        self.player_number = player_number
        self.player_level = player_level # e for easy, m for medium, h for hard, p if player
        self.moves_count = 0
        self.player_won = False
        self.queen = None
    def __repr__(self):
        return "(Pieces: " + str(self.unplaced_pieces) + ", Queen: " + str(self.queen) + ")"
    def get_level(self):
        return self.player_level

    def get_moves_count(self):
        return self.moves_count

    def get_player_number(self):
        return self.player_number

    def get_placed_pieces(self):
        placed_pieces = {piece for piece in self.placed_pieces if piece.get_player_number() == self.get_player_number()}
        return placed_pieces

    def get_queen(self):
        return self.queen

    def queen_unplaced(self):
        return not bool(self.get_queen())

    def set_queen(self, cell: CellPosition):
        self.queen = cell

    def update_available_pieces(self, from_cell, to_cell):
        # Make sure this is called AFTER the piece is moved in GameState.update_state()
        # bad design
        # but oh well
        if not from_cell:
            self.unplaced_pieces.update(to_cell.get_top_piece())
        else:
            self.placed_pieces.remove(from_cell)
        self.placed_pieces.append(to_cell)
    def undo_available_pieces(self, from_cell, to_cell):
        # Make sure this is called BEFORE the piece is moved in GameState.undo_state()
        # bad design
        # but oh well
        if not from_cell:
            self.unplaced_pieces.add_back(to_cell.get_top_piece())
        else:
            self.placed_pieces.append(from_cell)
        self.placed_pieces.remove(to_cell)
    def is_there_allowed_moves_for_player(self, board_state, current_allowed_moves):
        found_moves = False
        if not self.get_queen():
            return found_moves

        placed_pieces = self.get_placed_pieces()
        for from_cell in placed_pieces:
            available_moves = from_cell.get_available_moves(board_state)
            if available_moves:
                current_allowed_moves[from_cell] = available_moves
                found_moves = True

        return found_moves

    def get_unplaced_pieces(self):
        return self.unplaced_pieces