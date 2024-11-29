class CellPosition:
    dq_odd = [0, 1, 1, 1, 0, -1]
    dr_odd = [-1, -1, 0, 1, 1, 0]
    dq_even = [-1, 0, 1,0,-1,-1]
    dr_even = [-1, -1, 0,1,1,0]


    def __init__(self, r, q):
        """
        Represents a position on the grid.
        :param q: Column value
        :param r: Row value
        """
        self.r = r  # Row value
        self.q = q  # Column value
        self.pieces = []

    def __eq__(self, other):
        return self.q == other.q and self.r == other.r

    def __hash__(self):
        return hash((self.q, self.r))  # Hash based on the tuple (q, r)

    def __str__(self):
        """
        Custom string representation for CellPosition.
        """
        # # return f"({self.q}, {self.r})"
        # return "[" + str(self.get_top_piece()) + f"| ({self.q}, {self.r})]"
        return str(self.get_top_piece()) + f",{self.q},{self.r}"

    def __repr__(self):
        """
        Custom string representation for CellPosition.
        """
        return str(self.get_top_piece()) + f",{self.q},{self.r}"


    def is_occupied(self):
        return len(self.pieces) > 0

    def add_piece(self, piece):
        if piece:
            self.pieces.append(piece)

    def remove_piece(self):
        if self.pieces:
            return self.pieces.pop()
        return None

    def get_top_piece(self):
        if self.pieces:
            return self.pieces[-1]
        return None

    def get_player(self):
        if self.pieces:
            return self.pieces[-1].get_player()
        return None

    def get_name(self):
        if self.pieces:
            return self.pieces[-1].get_name()
        return None

    def get_all_pieces(self):
        return self.pieces

    def get_height(self):
        return len(self.pieces)

    @staticmethod
    def create_board():
        return [[CellPosition(r, q) for q in range(50)] for r in range(50)] #cell or cell position

    @staticmethod
    def get_center_of_board(game_board):
        return game_board[25][25]


    def get_neighbors(self, game_board):
        """
        Returns the neighboring CellPosition objects for the current position.
        """
        neighbors = []
        for i in range(len(CellPosition.dq_odd)):
            if self.r % 2 == 1:# Loop over the direction offsets
                new_q = self.q + CellPosition.dq_odd[i]
                new_r = self.r + CellPosition.dr_odd[i]
            else:
                new_q = self.q + CellPosition.dq_even[i]
                new_r = self.r + CellPosition.dr_even[i]

            if 0 <= new_q < 50 and 0 <= new_r < 50:
                neighbors.append(game_board[new_r][new_q])
        return neighbors

    def get_occupied_neighbors(self, game_board):
        neighbors = self.get_neighbors(game_board)
        neighbors = [neighbor for neighbor in neighbors if neighbor.is_occupied()]
        return neighbors

    def get_unoccupied_neighbors(self, game_board):
        neighbors = self.get_neighbors(game_board)
        neighbors = [neighbor for neighbor in neighbors if not neighbor.is_occupied()]
        return neighbors

    def get_diagonals(self, game_board):
        diagonals =  [[] for _ in range(6)]
        for i, diagonal in enumerate(diagonals):
            old_q, old_r = self.q, self.r
            while(0 <= old_q < 50 and 0 <= old_r < 50):
                if old_r % 2 == 1:
                    new_q = old_q + CellPosition.dq_odd[i]
                    new_r = old_r + CellPosition.dr_odd[i]
                else:
                    new_q = old_q + CellPosition.dq_even[i]
                    new_r = old_r + CellPosition.dr_even[i]
                diagonal.append(game_board[old_r][old_q])
                old_q, old_r = new_q, new_r

        return diagonals

    def generate_paths(self, length, game_board, get_all_paths=False):
        """
        Generate all paths of a given length from a starting hex.

        Parameters:
        - start: The starting hex (can be any hashable identifier).
        - length: The desired path length (number of steps).
        - get_neighbors: A function that takes a hex and returns its neighbors.

        Returns:
        - A list of paths, where each path is a list of hexes.
        """
        def dfs(current_path):
            if len(current_path) == length + 1 or get_all_paths:
                all_paths.append(list(current_path))
                if (len(current_path)) == length + 1:
                    return

            neighbors = current_path[-1].get_neighbors(game_board)
            for neighbor in neighbors:
                if neighbor not in current_path  \
                  and not neighbor.is_occupied()  \
                  and neighbor.get_occupied_neighbors(game_board):  # Don't break one-hive too much
                    current_path.append(neighbor)
                    dfs(current_path)
                    current_path.pop()  # Backtrack

        all_paths = []
        dfs([self])
        return all_paths

    @staticmethod
    def get_same_color_cells(board, player_color: int):
        same_color = set()
        for row in board:
            for cell in row:
                if cell.is_occupied() and cell.get_player() == player_color:
                    same_color.add(cell)
        return same_color

    def get_hive(self, game_board, visited=None):
        if visited is None:
            visited = set()
        visited.add(self)
        neighbors = self.get_occupied_neighbors(game_board)
        for neighbor in neighbors:
            if neighbor not in visited:
                neighbor.get_hive(game_board, visited)
        return visited

    def is_a_bridge(self, game_board):
        neighbors = set(self.get_occupied_neighbors(game_board))
        tested_piece = self.remove_piece()

        rest_of_hive = self.get_hive(game_board)

        self.add_piece(tested_piece)

        return bool(neighbors.difference(rest_of_hive))



# TODO:
# a general dfs function with a level parameter because this is annoying
# (queen 1 level, beetle 1 level, spider 3 levels, ant infinite levels)
# ant needs DFS in case hive is in the shape of a donut or two donuts or whatever.
# grasshopper will need its own.. stuff. it moves like a rook.
