import pygame as pg
import settings
import scoreBoard



class TextObject():
    """Class that generates and renders a line of text."""
    def __init__(self,
                 fontName: str,
                 fontSize: int,
                 fontColor: tuple[float,float,float],
                 text: str = "",
                 defaultPosition: tuple[float,float] = (50,50)
                 ) -> None:

        
        self.fontName = fontName
        self.fontSize = fontSize
        self._fontColor = fontColor
        self._text = text

        self.defaultPosition = defaultPosition
        """The default position this textobject is rendered at."""

        self.GenerateFont(self.fontName,self.fontSize)
        self.GenerateText(self._text)


    def GenerateFont(self,fontName,fontSize):
        """Creates a font object for this textobject."""
        self.font = pg.font.SysFont(fontName,fontSize)

    def GenerateText(self,text,antiAilias: bool = True):
        """Creates a text surface for this textobject."""
        self.textObject = self.font.render(text,antiAilias,self._fontColor)


    def RenderText(self,
                   displaySurface: pg.surface,
                   position: tuple[float,float] = None
                   ):
        """Displays this text on its displaysurface at the given position."""

        if position == None:
            position = self.defaultPosition

        displaySurface.blit(self.textObject,position)


    def GetColor(self):
        return self._fontColor
    def SetColor(self,color: tuple[float,float,float]):
        self._fontColor = tuple(int(component) for component in color) # chatgpt helped me fix an error i was getting here because i was using floats
        self.GenerateText(self._text)

    color = property(GetColor,SetColor)

    def GetText(self):
        return self._text
    def SetText(self,inputText):
        self._text = inputText
        self.GenerateText(self._text)
        
    text = property(GetText,SetText)







        
mainFontName: str =  "Comic Sans"



class TextHandler():
    """
    An object that contains references to a number
    of textobjects and can render them
    """
    def __init__(self,displaySurface : pg.surface, textList: dict[str : TextObject] = {}) -> None:

        self.displaySurface = displaySurface
        self.textList = textList

    def CreateTextObject(self,
                 textReferenceName: str,
                 fontName: str,
                 fontSize: int,
                 fontColor: tuple[float,float,float],
                 text: str = "",
                 defaultPosition: tuple[float,float] = (50,50)
                 ) -> None:
        self.textList[textReferenceName] = TextObject(fontName,fontSize,fontColor,text,defaultPosition=defaultPosition) # add thet textobject to the textlist

    def RenderText(self,
                   textReferenceName: str,
                   position: tuple[float,float] = None):
        """Render text using a text reference string."""

        self.textList[textReferenceName].RenderText(self.displaySurface,position)

    def RenderTextobject(self,textObject: TextObject, position: tuple[float,float] = None) -> None:
        """Renders text using a TextObject."""
        textObject.RenderText(self.displaySurface,position)


    def GetTextObjectsFromDicts(
            self,
            entryList: list[dict[str:str]],
            topLeftPosition: tuple[float,float] = (50,50), # the position where the first entry is rendered
            yPositionOffset: float = 50, # ho much each row is offset from the last
            maxEntries: int = 10,

            
            ) -> list[TextObject]:
        """Takes a dict with socreboard entries and returns a list of renderable text objects."""

        TextObjectList = []


        for index,entry in enumerate(entryList):
            text = str(index+1) + ". " # the list is sorted after score (by default at least)
            for key,value in entry.items():
                text = text + key + ": " + value + ", " # Add each attribute of the entry to a string

            TextObjectList.append(TextObject(mainFontName,statFontSize,fontColor=statFontColor,text=text,defaultPosition=(topLeftPosition[0],topLeftPosition[1]+index*yPositionOffset)))

            # stop iterating through dicts when maxentries has been reached
            if index >= maxEntries -1:
                break


        return TextObjectList




wonFontSize: int = 90
wonFontColor: tuple[float,float,float] = (255,255,255)
wonTextPosition: tuple[float,float] = (settings.WIDTH/2,100)

wonText: str = "You Won!"
returnText: str = "To return to the main menu, Press P."

statFontSize: int = 30
statFontColor: tuple[float,float,float] = (255,255,255)
statTextPosition: tuple[float,float] = (settings.WIDTH/2,200)
statTextRowOffset: float = 75 

statTimeBaseText = "Your time:"
statMovesBaseText = "Your amount of moves:"
statTotalScoreBaseText = "Your total score is:"


class WonTextManager(TextHandler):
    """Class that renders text at the end of the memory game. Inherits from the textHandler class"""
    def __init__(self,displaySurface : pg.surface, textList: dict[str : TextObject] = {}) -> None:
        
        # reference strings for all textobjects
        self.wonTextReference = "wonText"
        self.statTextReference = "statText"
        self.scoreTextReference = "scoreText"
        self.returnTextReference = "playAgain"

        super().__init__(displaySurface,{
            self.wonTextReference:TextObject(mainFontName,wonFontSize,wonFontColor,wonText),
            self.returnTextReference:TextObject(mainFontName,statFontSize,statFontColor,returnText),
            })

        



    def RenderEndgameText(self) -> None:
        """Renders the text """
        self.RenderText(self.wonTextReference,wonTextPosition)
        self.RenderText(self.statTextReference,statTextPosition)
        self.RenderText(self.scoreTextReference,(statTextPosition[0],statTextPosition[1]+statTextRowOffset))
        self.RenderText(self.returnTextReference,(statTextPosition[0],statTextPosition[1]+statTextRowOffset*2))
        


    def CreateStatText(self, time, guesses, totalScore) -> None: 
        """Create the rendered text object for the players stats."""
        self.CreateTextObject(self.statTextReference,mainFontName,statFontSize,statFontColor,f"{statTimeBaseText} {round(time,1)}, {statMovesBaseText} {guesses}")
        self.CreateTextObject(self.scoreTextReference,mainFontName,statFontSize,statFontColor,f"{statTotalScoreBaseText} {totalScore}")





    
        


    


