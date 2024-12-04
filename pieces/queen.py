from .piece import Piece

class Queen(Piece):
    def __init__(self, player):
        super().__init__(player)
        self.name = "Q"

    def get_available_moves(self, cell, game_board):
        available_positions = set()

        if cell.is_a_bridge(game_board):
            return available_positions

        available_paths = cell.generate_paths(1, game_board)
        available_paths = [path for path in available_paths if self.is_path_valid(cell, path, game_board)]

        available_positions.update([path[-1] for path in available_paths])
        return available_positions

    
