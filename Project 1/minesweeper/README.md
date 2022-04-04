# 💻 Minesweeper #
Write an AI to play Minesweeper.
## 🔶 Understanding ##
There are two main files in this project: `runner`.py and `minesweeper.py`. `minesweeper.py` contains all of the logic the game itself and for the AI to play the game. `runner.py` has been implemented for you, and contains all of the code to run the graphical interface for the game. Once you’ve completed all the required functions in `minesweeper.py`, you should be able to run `python runner.py` to play Minesweeper (or let your AI play for you)!

Let’s open up `minesweeper.py` to understand what’s provided. There are three classes defined in this file,  `Minesweeper`, which handles the gameplay; `Sentence`, which represents a logical sentence that contains both a set of `cells` and a `count`; and `MinesweeperAI`, which handles inferring which moves to make based on knowledge.

The `Minesweeper` class has been entirely implemented for you. Notice that each cell is a pair `(i, j)` where i is the row number (ranging from 0 to height - 1) and j is the column number (ranging from 0 to width - 1).

The `Sentence` class will be used to represent logical sentences of the form described in the Background. Each sentence has a set of `cells` within it and a `count` of how many of those cells are mines. The class also contains functions `known_mines` and `known_safes` for determining if any of the cells in the sentence are known to be mines or known to be safe. It also contains functions `mark_mine` and `mark_safe` to update a sentence in response to new information about a cell.

Finally, the `MinesweeperAI` class will implement an AI that can play Minesweeper. The AI class keeps track of a number of values. `self.moves_made` contains a set of all cells already clicked on, so the AI knows not to pick those again. `self.mines` contains a set of all cells known to be mines. `self.safes` contains a set of all cells known to be safe. And `self.knowledge` contains a list of all of the Sentences that the AI knows to be true.

The `mark_mine` function adds a cell to `self.mines`, so the AI knows that it is a mine. It also loops over all sentences in the AI’s `knowledge` and informs each sentence that the cell is a mine, so that the sentence can update itself accordingly if it contains information about that mine. The `mark_safe` function does the same thing, but for safe cells instead.

