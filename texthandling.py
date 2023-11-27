import pygame as pg
import settings


mainFontName: str =  "Comic Sans"

wonFontSize: int = 90
wonFontColor: tuple[float,float,float] = (255,255,255)
wonTextPosition: tuple[float,float] = (settings.WIDTH/2,100)

wonText: str = "You Won!"

statFontSize: int = 30
statFontColor: tuple[float,float,float] = (255,255,255)
statTextPosition: tuple[float,float] = (settings.WIDTH/2,200)

statTimeBaseText = "Your time:"
statMovesBaseText = "Your amount of moves:"

        



class TextManager():
    """Class that renders text at the end of the memory game."""
    def __init__(self,displaySurface: pg.Surface) -> None:
        self.mainFont = pg.font.SysFont(mainFontName,wonFontSize)
        self.mainText = self.mainFont.render(wonText,True,wonFontColor)

        self.displaySurface = displaySurface

        self.statFont = pg.font.SysFont(mainFontName,statFontSize)

    def RenderEndgameText(self):
        """Renders the text """
        self.displaySurface.blit(self.mainText,wonTextPosition)
        self.displaySurface.blit(self.statText,statTextPosition)
        


    def CreateStatText(self, time, guesses): 
        """Create the rendered text object for the players stats."""
        self.statText = self.statFont.render(f"{statTimeBaseText} {round(time,1)}, {statMovesBaseText} {guesses}",True,statFontColor)



