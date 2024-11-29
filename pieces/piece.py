from Core.cell_position import CellPosition

class Piece:
    def __init__(self, player):
        self.name = "ANY"
        self.player = player

    def __eq__(self, other):
        if isinstance(other, Piece):
            return self.name == other.name and self.player == other.player
        return False

    def __str__(self):
        return f"{self.name}-P{self.player}"

    def get_name(self):
        return self.name

    def get_player(self):
        return self.player

    def get_available_placements(self, game_board):
        """checks that the piece placed will be connected to one's color ONLY"""
        available_positions = set()
        same_color_positions = CellPosition.get_same_color_cells(game_board, self.get_player())
        for position in same_color_positions:
            neighbors = position.get_neighbors(game_board)

            different_color_neighbors = []

            for neighbor in neighbors:
                if neighbor.is_occupied() and neighbor.get_player() != self.get_player():
                    different_color_neighbors.append(neighbor)

            if different_color_neighbors:
                continue

            neighbors = [neighbor for neighbor in neighbors if not neighbor.is_occupied()]
            available_positions.update(neighbors)
        return available_positions

    def get_available_moves(self, cell, game_board):
        pass

    def breaks_one_hive(self, position_a, position_b, game_board, use_height):
        if use_height:
            if position_a.get_height() > 1:
                return False

        unoccupied_neighbors = set(position_a.get_unoccupied_neighbors(game_board))
        occupied_neighbors = set(position_a.get_occupied_neighbors(game_board))

        neighbors_of_occupied_neighbors = set()
        for neighbor in occupied_neighbors:
            neighbors_of_occupied_neighbors.update(neighbor.get_neighbors(game_board))

        return position_b not in unoccupied_neighbors.intersection(neighbors_of_occupied_neighbors)

    def breaks_freedom_of_movement(self, position_a, position_b, game_board, use_height):
        a_neighbors = set(position_a.get_occupied_neighbors(game_board))
        b_neighbors = set(position_b.get_occupied_neighbors(game_board))
        blocking_cells = a_neighbors.intersection(b_neighbors)
        if use_height:
            for block in blocking_cells:
                if not position_a.get_height() < block.get_height() \
                  or not position_b.get_height() < block.get_height():
                    return False
            return True
        else:
            return len(blocking_cells) >= 2

    def is_path_valid(self, cell, path, game_board, use_height=False):
        top_piece = cell.remove_piece()
        for i in range(len(path) - 1):
            position_a, position_b = path[i], path[i + 1]
            if self.breaks_one_hive(position_a, position_b, game_board, use_height) \
              or self.breaks_freedom_of_movement(position_a, position_b, game_board, use_height):
                cell.add_piece(top_piece)
                return False
        cell.add_piece(top_piece)
        return True






