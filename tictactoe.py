X = "X"
O = "O"
EMPTY = None

def initial_state():
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]

def player(board):
    x_count = sum(row.count("X") for row in board)
    o_count = sum(row.count("O") for row in board)
    return "O" if x_count > o_count else "X"

def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    return {(i, j) for i in range(3) for j in range(3) if board[i][j] == EMPTY}

def result(board, action):
    i, j = action
    if board[i][j] != EMPTY:
        raise ValueError("Invalid move")
    new_board = [row[:] for row in board]  # Deep copy
    new_board[i][j] = player(board)
    return new_board

def winner(board):
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] != EMPTY:
            return board[i][0]
        if board[0][i] == board[1][i] == board[2][i] != EMPTY:
            return board[0][i]
    if board[0][0] == board[1][1] == board[2][2] != EMPTY:
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] != EMPTY:
        return board[0][2]
    return None

def terminal(board):
    return winner(board) is not None or all(cell != EMPTY for row in board for cell in row)

def utility(board):
    if winner(board) == "X":
        return 1
    elif winner(board) == "O":
        return -1
    else:
        return 0

def minimax(board):
    def max_value(board, alpha, beta):
        if terminal(board):
            return utility(board), None
        value = float('-inf')
        best_move = None
        for action in actions(board):
            min_val, _ = min_value(result(board, action), alpha, beta)
            if min_val > value:
                value = min_val
                best_move = action
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return value, best_move

    def min_value(board, alpha, beta):
        if terminal(board):
            return utility(board), None
        value = float('inf')
        best_move = None
        for action in actions(board):
            max_val, _ = max_value(result(board, action), alpha, beta)
            if max_val < value:
                value = max_val
                best_move = action
            beta = min(beta, value)
            if alpha >= beta:
                break
        return value, best_move

    current_player = player(board)
    if current_player == X:
        _, move = max_value(board, float('-inf'), float('inf'))
    else:
        _, move = min_value(board, float('-inf'), float('inf'))
    return move
