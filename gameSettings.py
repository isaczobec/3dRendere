"""Universal setting variables for the memory game."""

boardSize: tuple = (3,2)
"""The size in cards of the memory board."""

# if the amount of cards is not even, add a column
if boardSize[0] * boardSize[1] % 2 != 0:
    boardSize = (boardSize[0] + 1, boardSize[1])

cardOffset: tuple[int] = (4.5,4.5)
"""The position offset (x,z) between every memorycard. Used when the board is generated."""


flipCardSpeed = 150
"""How fast the cards will turn around."""

cardsTurnBackCooldown: float = 2
"""time in seconds until cards are turned back after turning up 2 cards"""

cardDimensionRatio: tuple = (1.364,1)
"""What dimensions (x,z) a memory card should have."""

cardBackSizeScaleFactor: float = 1.05
"""How much larger the cards backsides are. Done so that they wont show whats behind them."""

memoryCardYOffset: float = -17
"""how far down the memory cards will be placed."""