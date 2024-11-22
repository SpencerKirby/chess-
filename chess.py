"""
Spencer Kirby 8/9/23
chess
"
let = "ABCDEFGH"
turn = 1
board = [
    ["Rr", "Rk", "Rb", "RQ", "RK", "Rb", "Rk", "Rr"],
    ["Rp", "Rp", "Rp", "Rp", "Rp", "Rp", "Rp", "Rp"],
    ["0", "0", "0", "0", "0", "0", "0", "0"],
    ["0", "0", "0", "0", "0", "0", "0", "0"],
    ["0", "0", "0", "0", "0", "0", "0", "0"],
    ["0", "0", "0", "0", "0", "0", "0", "0"],
    ["Wp", "Wp", "Wp", "Wp", "Wp", "Wp", "Wp", "Wp"],
    ["Wr", "Wk", "Wb", "WQ", "WK", "Wb", "Wk", "Wr"]
]
white_king_moved = False
white_rook_king_moved = False
white_rook_queen_moved = False
black_king_moved = False
black_rook_king_moved = False
black_rook_queen_moved = False

# Checks the possible moves for a piece and includes castling logic for kings
def atk_sight(board, loc, color):
    piece = board[loc[0]][loc[1]]
    if piece == "0":
        return None
    ret = []

    if piece[0] == color:
        if piece[1] == "k":  # King moves in all directions by 1 square
            valid_moves = [[2, 1], [2, -1], [-2, 1], [-2, -1], [1, 2], [1, -2], [-1, 2], [-1, -2]]
            for r in valid_moves:
                tmp = [loc[0] + r[0], loc[1] + r[1]]
                if 0 <= tmp[0] < 8 and 0 <= tmp[1] < 8:  # Check boundaries
                    if board[tmp[0]][tmp[1]] == "0" or board[tmp[0]][tmp[1]][0] != color:  # Ensure not same color
                        ret.append(tmp)

        elif piece[1] == "r":  # Rook moves along rows and columns
            for direction in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                for i in range(1, 8):
                    new_loc = [loc[0] + i * direction[0], loc[1] + i * direction[1]]
                    if 0 <= new_loc[0] < 8 and 0 <= new_loc[1] < 8:
                        if board[new_loc[0]][new_loc[1]] == "0" or board[new_loc[0]][new_loc[1]][0] != color:
                            ret.append(new_loc)
                        if board[new_loc[0]][new_loc[1]] != "0":  # Stop if piece encountered
                            break
                    else:
                        break  # Stop if out of bounds

        elif piece[1] == "b":  # Bishop moves diagonally
            for direction in [(1, 1), (1, -1), (-1, 1), (-1, -1)]:
                for i in range(1, 8):
                    new_loc = [loc[0] + i * direction[0], loc[1] + i * direction[1]]
                    if 0 <= new_loc[0] < 8 and 0 <= new_loc[1] < 8:
                        if board[new_loc[0]][new_loc[1]] == "0" or board[new_loc[0]][new_loc[1]][0] != color:
                            ret.append(new_loc)
                        if board[new_loc[0]][new_loc[1]] != "0":  # Stop if piece encountered
                            break
                    else:
                        break  # Stop if out of bounds

        elif piece[1] == "Q":  # Queen moves like both rook and bishop
            for direction in [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]:
                for i in range(1, 8):
                    new_loc = [loc[0] + i * direction[0], loc[1] + i * direction[1]]
                    if 0 <= new_loc[0] < 8 and 0 <= new_loc[1] < 8:
                        if board[new_loc[0]][new_loc[1]] == "0" or board[new_loc[0]][new_loc[1]][0] != color:
                            ret.append(new_loc)
                        if board[new_loc[0]][new_loc[1]] != "0":  # Stop if piece encountered
                            break
                    else:
                        break  # Stop if out of bounds

        else:  # Pawn movement logic
            if piece[0] == "W":  # White pawn
                # Move forward one square if the square is empty
                if loc[0] > 0 and board[loc[0] - 1][loc[1]] == "0":
                    ret.append([loc[0] - 1, loc[1]])

                # Move forward two squares from starting position if both squares are empty
                if loc[0] == 6 and board[loc[0] - 1][loc[1]] == "0" and board[loc[0] - 2][loc[1]] == "0":
                    ret.append([loc[0] - 2, loc[1]])

                # Capture diagonally if the opponent's piece is present
                if loc[1] + 1 < 8 and board[loc[0] - 1][loc[1] + 1] != "0" and board[loc[0] - 1][loc[1] + 1][0] != color:  # Opponent's piece
                    ret.append([loc[0] - 1, loc[1] + 1])
                if loc[1] - 1 >= 0 and board[loc[0] - 1][loc[1] - 1] != "0" and board[loc[0] - 1][loc[1] - 1][0] != color:  # Opponent's piece
                    ret.append([loc[0] - 1, loc[1] - 1])

            else:  # Black pawn
                # Move forward one square if the square is empty
                if loc[0] < 7 and board[loc[0] + 1][loc[1]] == "0":
                    ret.append([loc[0] + 1, loc[1]])

                # Move forward two squares from starting position if both squares are empty
                if loc[0] == 1 and board[loc[0] + 1][loc[1]] == "0" and board[loc[0] + 2][loc[1]] == "0":
                    ret.append([loc[0] + 2, loc[1]])

                # Capture diagonally if the opponent's piece is present
                if loc[1] + 1 < 8 and board[loc[0] + 1][loc[1] + 1] != "0" and board[loc[0] + 1][loc[1] + 1][0] != color:  # Opponent's piece
                    ret.append([loc[0] + 1, loc[1] + 1])
                if loc[1] - 1 >= 0 and board[loc[0] + 1][loc[1] - 1] != "0" and board[loc[0] + 1][loc[1] - 1][0] != color:  # Opponent's piece
                    ret.append([loc[0] + 1, loc[1] - 1])

                if piece[0] == 'W' and not white_king_moved:
                    if not white_rook_king_moved and board[7][5] == "0" and board[7][6] == "0" and board[7][7] == "Wr" and not is_under_attack(board, [7, 4]) and not is_under_attack(board, [7, 5]) and not is_under_attack(board, [7, 6]):
                        ret.append([7, 6])
                    if not white_rook_queen_moved and board[7][1] == "0" and board[7][2] == "0" and board[7][3] == "0" and board[7][0] == "Wr" and not is_under_attack(board, [7, 4]) and not is_under_attack(board, [7, 3]):
                        ret.append([7, 2])
                elif piece[0] == 'R' and not black_king_moved:
                    if not black_rook_king_moved and board[0][5] == "0" and board[0][6] == "0" and board[0][7] == "Br" and not is_under_attack(board, [0, 4]) and not is_under_attack(board, [0, 5]) and not is_under_attack(board, [0, 6]):
                        ret.append([0, 6])
                    if not black_rook_queen_moved and board[0][1] == "0" and board[0][2] == "0" and board[0][3] == "0" and board[0][0] == "Br" and not is_under_attack(board, [0, 4]) and not is_under_attack(board, [0, 3]):
                        ret.append([0, 2])

    return ret

# Checks if a square or the king's path is under attack
def is_under_attack(board, loc):
    color = "R" if board[loc[0]][loc[1]][0] == "W" else "W"
    attack_squares = []
    
    for r in range(8):
        for c in range(8):
            piece = board[r][c]
            if piece != "0" and piece[0] != color:
                attack_squares += atk_sight(board, [r, c], color)

    return loc in attack_squares

# Displays the chessboard
def draw(board):
    print("\n |1|2|3|4|5|6|7|8|", end="")
    for r in range(0, 8):
        print("\n" + let[r], end="|")
        for c in range(0, 8):
            x = board[r][c]
            if x == "0":
                print(" |", end="")
            elif x[0] == "R":
                print("\033[91m {}\033[00m".format(x[1]).replace(' ', ''), end="|")
            else:
                print(x[1], end="|")

# Handles checkmate logic
def checkmate(board, color):
    kingloc = None
    for r in range(8):
        for c in range(8):
            if board[r][c][0] == color and board[r][c][1] == "K":
                kingloc = [r, c]
                break
        if kingloc:
            break

    if not kingloc:
        return False
    danger = []
    for r in range(8):
        for c in range(8):
            piece = board[r][c]
            if piece != "0" and piece[0] != color:
                danger += atk_sight(board, [r, c])

    if kingloc not in danger:
        return False

    valid_moves = [[-1, -1], [-1, 0], [-1, 1], [0, -1], [0, 1], [1, -1], [1, 0], [1, 1]]
    for move in valid_moves:
        new_row = kingloc[0] + move[0]
        new_col = kingloc[1] + move[1]

        if 0 <= new_row < 8 and 0 <= new_col < 8:
            if [new_row, new_col] not in danger and board[new_row][new_col] == "0":
                return False

    for r in range(8):
        for c in range(8):
            piece = board[r][c]
            if piece != "0" and piece[0] == color:
                valid_moves = atk_sight(board, [r, c])
                for move in valid_moves:
                    if move == kingloc:
                        continue
                    temp_board = [row[:] for row in board]
                    temp_board[move[0]][move[1]] = temp_board[r][c]
                    temp_board[r][c] = "0"
                    if not checkmate(temp_board, color):
                        return False

    return True

# Main game loop if you want to play it against human 
def runner():
    global turn, white_king_moved, white_rook_king_moved, white_rook_queen_moved, black_king_moved, black_rook_king_moved, black_rook_queen_moved

    print("To exit the game type 'exit'")
    while True:
        draw(board)
        color = 'W' if turn % 2 == 1 else 'R'
        print(f"{'White' if color == 'W' else 'Black'}'s turn")
        
        move = input("Enter your move (e.g., E2 E4): ")
        if move.lower() == 'exit':
            print("Exiting the game.")
            break

        try:
            start, end = move.split()
            start_row = let.index(start[0].upper())
            start_col = int(start[1]) - 1
            end_row = let.index(end[0].upper())
            end_col = int(end[1]) - 1

            piece = board[start_row][start_col]
            if piece == "0" or piece[0] != color[0]:
                print("Invalid starting position.")
                continue

            # Castling move handling
            if piece[1] == "K" and abs(start_col - end_col) == 2:
                if color == "W":
                    if start_col == 4 and end_col == 6:  # King-side castling
                        if white_king_moved or white_rook_king_moved:
                            print("You cannot castle because the king or rook has already moved.")
                            continue
                        white_king_moved = True
                        white_rook_king_moved = True
                    elif start_col == 4 and end_col == 2:  # Queen-side castling
                        if white_king_moved or white_rook_queen_moved:
                            print("You cannot castle because the king or rook has already moved.")
                            continue
                        white_king_moved = True
                        white_rook_queen_moved = True
                elif color == "R":
                    if start_col == 4 and end_col == 6:  # King-side castling
                        if black_king_moved or black_rook_king_moved:
                            print("You cannot castle because the king or rook has already moved.")
                            continue
                        black_king_moved = True
                        black_rook_king_moved = True
                    elif start_col == 4 and end_col == 2:  # Queen-side castling
                        if black_king_moved or black_rook_queen_moved:
                            print("You cannot castle because the king or rook has already moved.")
                            continue
                        black_king_moved = True
                        black_rook_queen_moved = True

                # Perform castling move
                board[end_row][end_col] = piece
                board[start_row][start_col] = "0"
                if end_col == 6:
                    board[end_row][end_col - 1] = board[end_row][7]
                    board[end_row][7] = "0"
                elif end_col == 2:
                    board[end_row][end_col + 1] = board[end_row][0]
                    board[end_row][0] = "0"
                turn += 1
                continue

            # Normal move handling
            valid_moves = atk_sight(board, [start_row, start_col], color)
            if [end_row, end_col] in valid_moves:
                board[end_row][end_col] = board[start_row][start_col]
                board[start_row][start_col] = "0"
                if piece[1] == "K":
                    if color == "W":
                        white_king_moved = True
                    else:
                        black_king_moved = True
                elif piece[1] == "R":
                    if color == "W" and start_col == 0:
                        white_rook_queen_moved = True
                    elif color == "W" and start_col == 7:
                        white_rook_king_moved = True
                    elif color == "R" and start_col == 0:
                        black_rook_queen_moved = True
                    elif color == "R" and start_col == 7:
                        black_rook_king_moved = True
                turn += 1
            else:
                print("Invalid move. Try again.")

        except ValueError:
            print("Invalid input. Please enter a valid move.")
