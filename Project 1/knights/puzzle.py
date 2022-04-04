from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# Puzzle 0
# A says "I am both a knight and a knave."
knowledge0 = And(
    #Each character is either a knight or a knave
    Not(And(AKnight, AKnave)), 
    Or(AKnight, AKnave),
    # A cannot be both a knight and a knave
    Biconditional(And(AKnave, AKnight), AKnight)
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
knowledge1 = And(
    #Each character is either a knight or a knave
    Not(And(AKnight, AKnave)), 
    Or(AKnight, AKnave),
    Not(And(BKnight, BKnave)), 
    Or(BKnight, BKnave),
    # They cannot be both knaves because that makes A's statement true. Which cannot happen since knave will always lie.
    Biconditional(And(AKnave, BKnave), AKnight)
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
knowledge2 = And(
    #Each character is either a knight or a knave
    Not(And(AKnight, AKnave)),
    Or(AKnight, AKnave),
    Not(And(BKnight, BKnave)),
    Or(BKnight, BKnave),
    # They cannot be same kind, they have contradictory statements. 
    Implication(AKnight, And(AKnight, BKnight)),
    Implication(AKnave, Not(And(AKnave, BKnave))),
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
knowledge3 = And(
     #Each character is either a knight or a knave
    Not(And(AKnight, AKnave)),
    Or(AKnight, AKnave),
    Not(And(BKnight, BKnave)),
    Or(BKnight, BKnave),
    Not(And(CKnight, CKnave)),
    Or(CKnight, CKnave),
    Biconditional(Or(AKnight, AKnave), Or(AKnight, AKnave)),
    Biconditional(Biconditional(AKnave,AKnight),BKnight),
    Biconditional(BKnight, CKnave),
    Biconditional(AKnight, CKnight)
)


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
