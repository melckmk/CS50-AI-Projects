import itertools
import random


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        # If number of cells is equal to the count, then all of that cells must be mines.
        # Else, which cell is a mine is unknown.
        if len(self.cells) == self.count:
            return self.cells
        else:
            return set()

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        # If count is 0, there is no mine in set.
        if self.count == 0:
            return self.cells
        else:
            return set()

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        # Check to see if cell is one of the cells included in the sentence. 
        if cell in self.cells:
            # If cell is in the sentence, should update the sentence so that cell is no longer in the sentence.
            self.cells.remove(cell)
            # Mark the cell as mine 
            self.count -= 1
        return

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        # Check to see if cell is one of the cells included in the sentence.
        if cell in self.cells:
            # If cell is in the sentence, should update the sentence so that cell is no longer in the sentence.
            self.cells.remove(cell)
        return

class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """
        # Mark the cell as one of the moves made in the game.
        self.moves_made.add(cell)
        # Mark the cell as a safe cell.
        self.mark_safe(cell)
        # Add a new sentence to the AI’s knowledge base based on the value of cell and count, to indicate that count of the cell’s neighbors are mines.
        # Get neighbors of the cell
        neighbors = self.get_neighbors(cell)
        new_sentence = Sentence(neighbors, count)
        # Mark additional cells as safe or mines.
        for mine in self.mines:
            new_sentence.mark_mine(mine)
        for safe in self.safes:
            new_sentence.mark_safe(safe)

        self.knowledge.append(new_sentence)
        
        mines = set()
        safes = set()
        for sentence in self.knowledge:
            for mine in sentence.known_mines():
                mines.add(mine)
            for safe in sentence.known_safes():
                safes.add(safe)
        
        for mine in mines:
            self.mark_mine(mine)
        for safe in safes:
            self.mark_safe(safe)
        # Add any new sentences to the AI's knowledge base if they can be inferred from existing knowledge
        self.remove_empty()
        self.inference()


    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        # The move returned must be known to be safe, and not a move already made.
        for cell in self.safes:
            if cell not in self.moves_made:
                return cell
        # If no safe move can be guaranteed, the function should return None.
        return None
        
    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        # This function will be called if a safe move is not possible
        # if the AI doesn’t know where to move, it will choose to move randomly instead.
        for i in range(0, self.height):
            for j in range(0, self.width):
                # The move must not be a move that has already been made and that is known to be a mine.
                if (i, j) not in self.mines and (i, j) not in self.moves_made:
                    return (i, j)
        # If no such moves are possible, the function should return None.
        return None

    def get_neighbors(self, cell):
        neighbors = set()
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):
                if (i,j) != cell:
                    if 0 <= i < self.height and 0 <= j < self.width:
                        neighbors.add((i,j))
        return neighbors
    
    def remove_empty(self):
        removed = []
        for sentence in self.knowledge:
            if sentence.cells == set():
                removed.append(sentence)
        for sentence in removed:
            self.knowledge.remove(sentence)

    def inference(self):
        for s1 in self.knowledge:
            for s2 in self.knowledge:
                if s1.cells == s2.cells:
                    continue
                if s1.cells.issubset(s2.cells):
                    new_cells = s2.cells - s1.cells
                    new_count = s2.count - s1.count
                    new_sentence = Sentence(new_cells, new_count)
                    if new_sentence not in self.knowledge:
                        self.knowledge.append(new_sentence)
        