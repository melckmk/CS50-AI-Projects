# 💻 Crossword #
Write an AI to generate crossword puzzles.
```
$ python generate.py data/structure1.txt data/words1.txt output.png
██████████████
███████M████R█
█INTELLIGENCE█
█N█████N████S█
█F██LOGIC███O█
█E█████M████L█
█R███SEARCH█V█
███████X████E█
██████████████
```
## 🔸 Understanding ##

There are two Python files in this project: `crossword.py` and `generate.py`.

First, let’s take a look at `crossword.py`. This file defines two classes, `Variable` (to represent a variable in a crossword puzzle) and `Crossword` (to represent the puzzle itself).

Notice that to create a `Variable`, we must specify four values: its row `i`, its column `j`, its direction (either the constant `Variable.ACROSS` or the constant `Variable.DOWN`), and its length.

The `Crossword` class requires two values to create a new crossword puzzle: a `structure_file` that defines the structure of the puzzle (the `_` is used to represent blank cells, any other character represents cells that won’t be filled in) and a `words_file` that defines a list of words (one on each line) to use for the vocabulary of the puzzle. Three examples of each of these files can be found in the `data` directory of the project, and you’re welcome to create your own as well.

Note in particular, that for any crossword object `crossword`, we store the following values:
- `crossword.height` is an integer representing the height of the crossword puzzle.
- `crossword.width` is an integer representing the width of the crossword puzzle.
- `crossword.structure` is a 2D list representing the structure of the puzzle. For any valid row `i` and column `j`, `crossword.structure[i][j]` will be `True` if the cell is blank (a character must be filled there) and will be `False` otherwise (no character is to be filled in that cell).
- `crossword.words` is a set of all of the words to draw from when constructing the crossword puzzle.
- `crossword.variables` is a set of all of the variables in the puzzle (each is a `Variable` object).
- `crossword.overlaps` is a dictionary mapping a pair of variables to their overlap. For any two distinct variables `v1` and `v2`, `crossword.overlaps[v1, v2]` will be `None` if the two variables have no overlap, and will be a pair of integers `(i, j)` if the variables do overlap. The pair `(i, j)` should be interpreted to mean that the `i`th character of `v1`’s value must be the same as the `j`th character of `v2`’s value.

Crossword objects also support a method `neighbors`  that returns all of the variables that overlap with a given variable. That is to say, `crossword.neighbors(v1)` will return a set of all of the variables that are neighbors to the variable `v1`.

Next, take a look at `generate.py`. Here, we define a class `CrosswordCreator` that we’ll use to solve the crossword puzzle. When a `CrosswordCreator` object is created, it gets a `crossword` property that should be a `Crossword` object (and therefore has all of the properties described above). Each `CrosswordCreator` object also gets a `domains` property: a dictionary that maps variables to a set of possible words the variable might take on as a value. Initially, this set of words is all of the words in our vocabulary, but we’ll soon write functions to restrict these domains.

Finally, notice the `solve` function. This function does three things: first, it calls `enforce_node_consistency` to enforce node consistency on the crossword puzzle, ensuring that every value in a variable’s domain satisfy the unary constraints. Next, the function calls `ac3` to enforce arc consistency, ensuring that binary constraints are satisfied. Finally, the function calls `backtrack` on an initially empty assignment (the empty dictionary `dict()`) to try to calculate a solution to the problem.
