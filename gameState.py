class CellPosition:
    def __init__(self, q, r):
        self.q = q  # column value
        self.r = r  # row value

class GameState:
    def __init__(self):
        self.state = [["" for _ in range(50)] for _ in range(50)] # state of the grid(initially all empty)
        self.q1 = CellPosition(-1,-1) # player 1 queen bee
        self.q2 = CellPosition(-1,-1) # player 2 queen bee
        self.turn = 1 # turn (1 > player 1 , 2 > player 2)
        self.player1Moves = 0 # number of moves player 1 played till now
        self.player2Moves = 0 # number of moves player 2 played till now










# Grasshopper piece >> g1,g2
# Ant piece >> p1,p2
# Spider piece >> s1,s2
# Beetle piece >> b1,b2
# Queen piece >> q1,q2