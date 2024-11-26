from gameState import CellPosition
for i in range(7):
    for j in range(7):
       print("Neighbours of ",i," ",j,": ")
       neighbours = CellPosition(i,j).get_neighbors()
       for neighbour in neighbours:
           print(neighbour,end=',')
       print()
       print("*"*30)