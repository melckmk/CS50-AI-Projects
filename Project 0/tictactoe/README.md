# :computer: Tic-Tac-Toe #

Using Minimax, implement an AI to play Tic-Tac-Toe optimally.

## :small_orange_diamond: Understanding ##
There are two main files in this project: `runner.py` and `tictactoe.py`. `tictactoe.py` contains all of the logic for playing the game, and for making optimal moves. `runner.py` has been implemented for you, and contains all of the code to run the graphical interface for the game. Once you’ve completed all the required functions in `tictactoe.py`, you should be able to run python runner.py to play against your AI!

Let’s open up `tictactoe.py` to get an understanding for what’s provided. First, we define three variables: `X`, `O`, and `EMPTY`, to represent possible moves of the board.

The function `initial_state` returns the starting state of the board. For this problem, we’ve chosen to represent the board as a list of three lists (representing the three rows of the board), where each internal list contains three values that are either `X`, `O`, or `EMPTY`.
