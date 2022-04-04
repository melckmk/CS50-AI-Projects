from collections import deque
import sys

from crossword import *


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        w, h = draw.textsize(letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        # making sure that every value in a variable’s domain has the same number of letters as the variable’s length
        for var in self.domains:
            for value in self.domains[var].copy():
                if len(value) != var.length:
                    self.domains[var].remove(value)

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        # with the help of psudocode in lecture3 slide.
        revised = False
        overlap = self.crossword.overlaps[x, y]
        if overlap:
            i, j = overlap
            for word_x in self.domains[x].copy():
                check_if_overlaps = False
                for word_y in self.domains[y]:
                    if word_x[i] == word_y[j]:
                        check_if_overlaps = True
                if not check_if_overlaps:
                    self.domains[x].remove(word_x)
                    revised = True 
                    
        return revised    

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        # with the help of psudocode in lecture3 slide.
        if not arcs:
            # If arcs is None, start with an initial queue of all of the arcs in the problem.
            arcs = []
            for var in self.crossword.variables:
                for neighbor in self.crossword.neighbors(var):
                    arcs.append((var, neighbor))
        else:
            arcs = deque(arcs)

        while arcs:
            x, y = arcs.pop()
            if self.revise(x ,y):
                if len(self.domains[x]) == 0:
                    return False
                for z in self.crossword.neighbors(x) - {y}:
                    arcs.append((z, x))
        return True

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        for var in self.domains:
            if var not in assignment:
                return False
        return True

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        for var, word in assignment.items():
            # Check if every value is the correct length
            if var.length != len(word):
                return False
            # Check if all values are distinct
            for key, value in assignment.items():
                if var != key:
                    if word == value:
                        return False
            # Check if there are no conflicts between neighboring variables.
            for neighbor in self.crossword.neighbors(var):
                if neighbor in assignment.keys():
                    i, j = self.crossword.overlaps[var, neighbor]
                    if neighbor in assignment:
                        if word[i] != assignment[neighbor][j]:
                            return False
        return True

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        heuristics = {}
        neighbors = self.crossword.neighbors(var)
        for word in self.domains[var]:
            # Any variable present in assignment already has a value, shouldn't be counted.
            if word not in assignment:
                ruled_out = 0
                for neigbor in neighbors:
                    if word in self.domains[neigbor]:
                        ruled_out += 1
                heuristics[word] = ruled_out
        return sorted(heuristics, key=lambda key: heuristics[key])
                
    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        # Helper functions for getting length of neigbors and domain size.
        def degree(var):
            return len(self.crossword.neighbors(var))
        def domain(var):
            return len(self.domains[var])

        unassigned = []
        for var in self.crossword.variables:
            if var not in assignment:
                unassigned.append(var)

        result_var = unassigned[0]
        for var in unassigned:
            if result_var != var:
                # Return the variable with the fewest number of remaining values in its domain.
                if domain(result_var) > domain(var):
                    result_var = var
                # If there is a tie, choose the variable with the highest degree.
                elif domain(result_var) == domain(var):
                    if degree(var) >= degree(result_var):
                        result_var = var
        return result_var

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        # with the help of psudocode in lecture3 slide.
        # Return a complete assignment if possible to do so
        if self.assignment_complete(assignment):
            return assignment

        unassigned_vars = self.select_unassigned_variable(assignment)
        for value in self.order_domain_values(unassigned_vars, assignment):
            assignment[unassigned_vars] = value
            if self.consistent(assignment):
                result = self.backtrack(assignment)
                if result:
                    return result
            del assignment[unassigned_vars]

        return None

def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
