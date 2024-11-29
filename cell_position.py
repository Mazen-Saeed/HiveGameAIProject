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

    def is_occupied(self):
        return len(self.pieces) > 0

    def add_piece(self, piece):
        self.pieces.append(piece)

    def remove_piece(self):
        if self.pieces:
            return self.pieces.pop()
        return None

    def get_top_piece(self):
        if self.pieces:
            return self.pieces[-1]
        return None

    def get_all_pieces(self):
        return self.pieces

    def get_piece_height(self):
        return len(self.pieces)

    @staticmethod
    def create_board():
        return [[CellPosition(r, q) for q in range(50)] for r in range(50)] #cell or cell position

    @staticmethod
    def get_center_of_board(game_board):
        return game_board[25][25]

    @staticmethod
    def get_same_color_cells(board, player_color: int):
        same_color = set()
        for row in board:
            for cell in row:
                if cell.is_occupied() and cell.get_top_piece().player == player_color:
                    same_color.add(cell)
        return same_color

    def check_for_disconnection_upon_removal(self):
        #dfs from each neighbor and make sure cells match?
        #6 DFSs?
        #1 DFS from some neighbor (without self) and check that all neighbors were seen?
        pass

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

# TODO:
# a general dfs function with a level parameter because this is annoying
# (queen 1 level, beetle 1 level, spider 3 levels, ant infinite levels)
# ant needs DFS in case hive is in the shape of a donut or two donuts or whatever.
# grasshopper will need its own.. stuff. it moves like a rook.
