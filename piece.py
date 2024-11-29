from cell_position import CellPosition

class Piece:
    """
     Pieces in the game:
     Grasshopper pieces >> g1, g2
     Ant pieces >> a1, a2
     Spider pieces >> s1, s2
     Beetle pieces >> b1, b2
     Queen pieces >> q1, q2
    """

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
        """checks that the piece placed will be connected to one's color"""
        available_positions = set()
        same_color_positions = CellPosition.get_same_color_cells(game_board, self.get_player)
        for position in same_color_positions:
            neighbors = position.get_neighbors(game_board)
            neighbors = [neighbor for neighbor in neighbors if not neighbor.is_occupied()]
            available_positions.update(neighbors)
        return available_positions

    def get_available_moves(self, cell, game_board):
        pass

    def move_once_respecting_one_hive(self, cell, game_board):
        neighbors = cell.get_neighbors(game_board)
        unoccupied_neighbors = {neighbor for neighbor in neighbors if not neighbor.is_occupied()}

        occupied_neighbors = {neighbor for neighbor in neighbors if neighbor.is_occupied()}
        neighbors_of_occupied_neighbors = set()
        for neighbor in occupied_neighbors:
            neighbors_of_occupied_neighbors.update(neighbor.get_neighbors(game_board))

        return unoccupied_neighbors.intersection(neighbors_of_occupied_neighbors)


    def does_it_break_one_hive(self, cell):
        if cell.get_piece_height() > 1:
            return False
        return False
        pass

    def can_it_move_from(self, cell):
        """
        check also if surrounded by too many neighbors to move
        """
        return True
        pass

    def can_it_move_to(self, cell):
        """
        check if target piece is surrounded by too many neighbors: accounts for beetle via height of stack
        """
        return True
        pass

class Grasshopper(Piece):
    def __init__(self, player):
        self.name = "G"
        self.player = player

    def get_available_moves(self, cell, game_board):
        available_positions = set()
        if not self.does_it_break_one_hive(cell):
            return available_positions

        diagonals = cell.get_diagonals(game_board)
        diagonals = [diagonal[2:] for diagonal in diagonals if len(diagonal) > 2 and diagonal[1].is_occupied()]
        for diagonal in diagonals:
            for cell in diagonal:
                if not cell.is_occupied():
                    available_positions.add(cell)
                    break
        return available_positions


class Beetle(Piece):
    def __init__(self, player):
        self.name = "B"
        self.player = player
    def get_available_moves(self, cell, game_board):
        available_positions = set()

        if self.does_it_break_one_hive(cell):
            return available_positions

        neighbors = cell.get_neighbors(game_board)

        # A beetle can go anywhere from on top of the hive
        if cell.get_piece_height() > 1:
            available_positions.update(neighbors)
            return available_positions

        available_positions.update(self.move_once_respecting_one_hive(cell, game_board))
        available_positions = {position for position in available_positions if self.can_it_move_to(position)}

        occupied_neighbors = {neighbor for neighbor in neighbors if neighbor.is_occupied()}

        available_positions.update(occupied_neighbors)
        return available_positions

        # check link on discord about small holes
        # beetle is HARD



class Ant(Piece):
    def __init__(self, player):
        self.name = "A"
        self.player = player
    def get_available_moves(self, cell, game_board):
        available_positions = set()
        if self.does_it_break_one_hive(cell):
            return available_positions
        if not self.can_it_move_from(cell):
            return available_positions

        # rules here
        """
        Same questions about the spider and the one-hive rule.

        I know if a place is too narrow, the ant just bounces off and can keep moving
        as illustrated in the rule-book.
        """
        available_positions = {position for position in available_positions if self.can_it_move_to(position)}

class Spider(Piece):
    def __init__(self, player):
        self.name = "S"
        self.player = player

    def get_available_moves(self, cell, game_board):
        available_positions = set()
        """
        if not self.does_it_break_one_hive(cell):
            return available_positions
        if not self.can_it_move_from(cell):
            return available_positions

        If a spider connects two islands but stays in the middle while moving, does that break one-hive?

        Can some location reached in the middle by spider be too narrow? do I have to check
        can_it_move_to for every cell on its 3-length path?

        """
        neighbors = cell.get_neighbors(game_board)
        unoccupied_neighbors = [neighbor for neighbor in neighbors if not neighbor.is_occupied()]
        available_positions.update(unoccupied_neighbors)

        for i in range(2):
            unoccupied_neighbors = set()
            for neighbor in available_positions:
                neighbors = neighbor.get_neighbors(game_board)
                unoccupied_neighbors.update([neighbor for neighbor in neighbors if not neighbor.is_occupied()])
            available_positions.update(unoccupied_neighbors)

        available_positions = {position for position in available_positions if self.can_it_move_to(position)}
        return available_positions


class Queen(Piece):
    def __init__(self, player):
        self.name = "Q"
        self.player = player

    def get_available_moves(self, cell, game_board):
        #TODO: doesn't follow one-hive rule
        available_positions = set()
        if self.does_it_break_one_hive(cell):
            return available_positions
        if not self.can_it_move_from(cell):
            return available_positions

        available_positions.update(self.move_once_respecting_one_hive(cell, game_board))
        # This whole thing is to make sure one-hive rule is followed

        available_positions = {position for position in available_positions if self.can_it_move_to(position)}
        return available_positions


# TODO:
# When getting neighbors of neighbors, remove self! Also create a "visited" list bc this is necessary
