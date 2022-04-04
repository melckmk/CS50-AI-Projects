"""
Tic Tac Toe Player
"""

import math
import copy # Import copy for deepcopy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    num_x = 0
    num_o = 0

    for i in range(0,len(board)):
        for j in range(0,len(board[0])):
            if board[i][j] == X:
                num_x += 1
            elif board[i][j] == O:
                num_o += 1

    if num_x > num_o:
        return O
    elif not terminal(board) and num_x == num_o:
        return X
    else:
        return None


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """

    # Create a set to return all possible actions on the board.
    actions_set = set()

    # Possible moves are any cells on the board that do not already have an X or an O in them.
    for i in range(0,len(board)):
        for j in range(0,len(board[i])):
            if board[i][j] == EMPTY:
                actions_set.add((i,j))
    return actions_set


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    # Check if the action is valid.
    if action not in actions(board):
        raise Exception("Not a valid action.")
    elif terminal(board):
        raise Exception("Game Over")
    else:
        # Make a deep copy of the board first before making any changes.
        result_board = copy.deepcopy(board)
        # Return new board state for given action.
        result_board[action[0]][action[1]] = player(board)

    return result_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2]:
            if board[i][0] == X:
                return X
            elif board[i][0] == O:
                return O
            else:
                return None
    for j in range(3):
        if board[0][j] == board[1][j] == board[2][j]:
            if board[0][j] == X:
                return X
            elif board[0][j] == O:
                return O
            else:
                return None
    if board[0][0] == board[1][1] == board[2][2]:
        if board[0][0] == X:
            return X
        elif board[0][0] == O:
            return O
        else:
            return None
    if board[2][0] == board[1][1] == board[0][2]:
        if board[2][0] == X:
            return X
        elif board[2][0] == O:
            return O
        else:
            return None
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) is not None or not any(j==EMPTY for i in board for j in i):
        return True
    else:
        return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if terminal(board):
        if winner(board) == X:
            return 1
        elif winner(board) == O:
            return -1
        else:
            return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None
    else:
        if player(board) == X:
            optimal_action = None
            v = float("-inf")
            for action in actions(board):
                min_val = min_value(result(board, action))
                if min_val > v:
                    v = min_val
                    optimal_action = action
        else:
            optimal_action = None
            v = float("inf")
            for action in actions(board):
                max_val = max_value(result(board, action))
                if max_val < v:
                    v = max_val
                    optimal_action = action
        return optimal_action


# Add max_value and min_value helper functions.
def max_value(board):
    if terminal(board):
        return utility(board)
    
    v = float('-inf')
    
    for action in actions(board):
        v = max(v, min_value(result(board, action)))
    return v


def min_value(board):
    if terminal(board):
        return utility(board)
    
    v = float('inf')
    
    for action in actions(board):
        v = min(v, max_value(result(board, action)))
 
    return v
