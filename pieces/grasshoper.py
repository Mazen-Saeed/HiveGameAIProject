from .piece import Piece

class Grasshopper(Piece):
    def __init__(self, player):
        super().__init__(player)
        self.name = "G"

    def get_available_moves(self, cell, game_board):
        available_positions = set()

        if cell.is_a_bridge(game_board):
            return available_positions

        diagonals = cell.get_diagonals(game_board)
        diagonals = [diagonal[2:] for diagonal in diagonals if len(diagonal) > 2 and diagonal[1].is_occupied()]
        for diagonal in diagonals:
            for cell in diagonal:
                if not cell.is_occupied():
                    available_positions.add(cell)
                    break
        return available_positions