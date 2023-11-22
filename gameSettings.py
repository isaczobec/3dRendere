"""Universal setting variables for the memory game."""

boardSize: tuple = (3,3)
"""The size in cards of the memory board."""

# if the amount of cards is not even, add a column
if boardSize[0] * boardSize[1] % 2 != 0:
    boardSize = (boardSize[0] + 1, boardSize[1])

cardOffset: tuple[int] = (3,3)
"""The position offset (x,z) between every memorycard. Used when the board is generated."""


flipCardSpeed = 50
"""How fast the cards will turn around."""