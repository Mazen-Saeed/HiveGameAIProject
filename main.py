from Core.game_state import GameState
from Core.cell_position import CellPosition

mygame = GameState()

def print_hexagonal(grid, max_rows=10, max_cols=10):
    for i, row in enumerate(grid[:max_rows]):
        row_to_print = row[:max_cols]
        offset = "      " * (i % 2)
        row_str = "      ".join(str(obj) for obj in row_to_print)
        print(offset + row_str)

print_hexagonal(mygame.state)
print(mygame.player_available_pieces)
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.patches as patches
while (True):
    print(f"Player {mygame.turn} type 'p' to place and 'm' to move.")
    type_of_turn = input().strip()

    if type_of_turn == "p":
        x2, y2, name = input("Enter 2 numbers and piece name (x2, y2, name): ").split()
        x2, y2 = int(x2), int(y2)
        print(mygame.get_allowed_cells())
        mygame.update_state(globals()[name](mygame.turn), mygame.state[y2][x2])

    elif type_of_turn == "m":
        x1, y1, x2, y2 = map(int, input("Enter 4 numbers (from x1, y1 to x2, y2): ").split())
        mygame.get_allowed_cells_given_the_piece_on_cell(mygame.state[y1][x1])
        print(mygame.current_allowed_moves)
        mygame.update_state(globals()["Piece"](mygame.turn), mygame.state[y2][x2], mygame.state[y1][x1])

        # Function to draw hexagonal grid
    def draw_hexagonal_grid(data, ax, hex_size=30, zoom=1):
        rows, cols = data[:10, :10].shape

        ax.clear()

        # Adjusting the hex size for zoom
        hex_size *= zoom
        # Calculate the width and height of the hexagons
        width = np.sqrt(3) * hex_size
        height = 3 / 2 * hex_size

        # Loop through each position in the grid
        for row in range(rows):
            for col in range(cols):
                # Calculate the x, y coordinates for the hexagon
                x = col * width #* np.sqrt(3) / 2  # Base x-position for rotated hexagons
                y = row * height

                text_color = plt.cm.viridis(hash(data[row, col].get_name()) % 256 / 255)
                if data[row, col].get_player() == 0:
                    backcolor = 'white'
                elif data[row, col].get_player() == 1:
                    backcolor = 'black'
                else:
                    backcolor = 'beige'
                # Apply odd-r layout by shifting every odd row
                if row % 2 == 1:
                    x += width / 2  # Shift odd rows vertically

                # Draw hexagon
                hexagon = patches.Polygon(hexagon_points(x, y, hex_size), closed=True, edgecolor='black', facecolor=backcolor, lw=1)
                ax.add_patch(hexagon)

                # Place the text inside the hexagon
                ax.text(x, y, str(data[row, col]), ha='center', va='center', fontsize=8, color=text_color)

        ax.set_aspect('equal')
        ax.set_axis_off()
        ax.relim()
        ax.autoscale_view()

    # Function to calculate the points of a hexagon with rotation
    def hexagon_points(x, y, size):
        # Rotate the hexagon 90 degrees by switching the coordinates
        points = []
        for i in range(6):
            angle = np.pi / 3 * i + np.pi / 2  # 90-degree rotation
            point = (x + size * np.cos(angle), y + size * np.sin(angle))
            points.append(point)
        return points

    # Input: 50x50 array with custom text
    data = np.array(mygame.state)

    # Set up the plot
    fig, ax = plt.subplots(figsize=(10, 10))

    # Draw the grid with zoom factor
    zoom_factor = 1
    draw_hexagonal_grid(data, ax, hex_size=50, zoom=zoom_factor)

    # Show the plot
    plt.show()

    print_hexagonal(mygame.state)
    for attribute, value in vars(mygame).items():
        if attribute == "state":
            continue
        print(f"{attribute}: {value}")

    print(mygame.state[2][2].generate_paths(3, mygame.state))
    print(mygame.must_place_queen_bee())
    print(mygame.check_for_a_winner())
