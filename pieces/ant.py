from piece import Piece

class Ant(Piece):
    def __init__(self, player):
        super().__init__(player)
        self.name = "A"

    def get_available_moves(self, cell, game_board):
        available_positions = set()

        if cell.is_a_bridge(game_board):
            return available_positions

        available_paths = cell.generate_paths(60, game_board, True)
        available_paths = [path[1:] for path in available_paths if self.is_path_valid(cell, path, game_board) and len(path) > 1]
        for path in available_paths:
            available_positions.update(path)

        return available_positions