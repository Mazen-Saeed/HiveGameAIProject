from gameState import GameState, Piece, CellPosition


# Initialize game state
game_state = GameState("p", "p", "p", "p")  # Both players are human with easy level


# Function to ask the user for piece selection and position
def ask_for_piece_and_position(player_turn):
    available_pieces = game_state.player1AvailablePieces if player_turn == 1 else game_state.player2AvailablePieces

    # Show available pieces for the current player
    print(f"\nPlayer {player_turn}'s Available Pieces:")
    print(f"Grasshoppers (g): {available_pieces.g}")
    print(f"Ants (a): {available_pieces.a}")
    print(f"Beetles (b): {available_pieces.b}")
    print(f"Spiders (s): {available_pieces.s}")
    print(f"Queen Bees (q): {available_pieces.q}")

    # Ask for the piece type to place
    while True:
        piece_name = input(
            "Which piece would you like to place? (g for Grasshopper, a for Ant, b for Beetle, s for Spider, q for Queen Bee): ").strip().lower()

        if piece_name in ['g', 'a', 'b', 's', 'q']:
            if piece_name == 'g' and available_pieces.g > 0:
                piece = Piece('g', player_turn)
                break
            elif piece_name == 'a' and available_pieces.a > 0:
                piece = Piece('a', player_turn)
                break
            elif piece_name == 'b' and available_pieces.b > 0:
                piece = Piece('b', player_turn)
                break
            elif piece_name == 's' and available_pieces.s > 0:
                piece = Piece('s', player_turn)
                break
            elif piece_name == 'q' and available_pieces.q > 0:
                piece = Piece('q', player_turn)
                break
            else:
                print(f"You don't have any {piece_name} pieces left. Please choose another.")
        else:
            print("Invalid piece choice. Please choose again.")

    # Get allowed moves for the piece type
    allowed_moves = game_state.get_allowed_cells()

    # Print allowed moves before asking for input
    print(f"\nAllowed moves for {piece.get_name().upper()}:")
    for move in allowed_moves:
        print(move)  # This will call the __str__ method of CellPosition and print (q, r) values

    # Ask for the position to place the piece
    while True:
        try:
            q = int(input("Enter the column (q) position to place the piece (0-49): "))
            r = int(input("Enter the row (r) position to place the piece (0-49): "))
            position = CellPosition(q, r)

            # Validate if the chosen position is one of the allowed moves
            if position in allowed_moves:
                break
            else:
                print(f"The selected cell {position} is not an allowed move. Please choose another.")
        except ValueError:
            print("Invalid input. Please enter numeric values for q and r.")

    return piece, position


# Main game loop for manual testing
while True:
    # Print current game state information
    print("\n--- Game State ---")
    print(f"Current Turn: Player {game_state.turn}")
    print(f"Player 1 Queen Bee Position: {game_state.q1}")
    print(f"Player 2 Queen Bee Position: {game_state.q2}")
    print(f"Player 1 Moves: {game_state.player1Moves}")
    print(f"Player 2 Moves: {game_state.player2Moves}")
    print(
        f"Player 1 Available Pieces: g={game_state.player1AvailablePieces.g}, a={game_state.player1AvailablePieces.a}, b={game_state.player1AvailablePieces.b}, s={game_state.player1AvailablePieces.s}, q={game_state.player1AvailablePieces.q}")
    print(
        f"Player 2 Available Pieces: g={game_state.player2AvailablePieces.g}, a={game_state.player2AvailablePieces.a}, b={game_state.player2AvailablePieces.b}, s={game_state.player2AvailablePieces.s}, q={game_state.player2AvailablePieces.q}")

    # Check if a player has won
    winner = game_state.check_for_a_winner()
    if winner != 0:
        print(f"Player {winner} wins!")
        break  # Exit the loop if there's a winner

    # Ask the current player to choose a piece and position
    piece, position = ask_for_piece_and_position(game_state.turn)

    # Update the game state with the chosen piece and position
    if position == game_state.q1 or position == game_state.q2:
        print(f"Player {game_state.turn} places their Queen Bee at {position}.")
    game_state.update_state(piece, CellPosition(-1, -1), position)
