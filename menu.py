"""Module with classes used in menus of the game."""

import pygame as pg
import texthandling as th
import inputHandler
from typing import List
import sys
import gameSettings
import Time
import scoreBoard

mainFont = "Comic Sans"


class Button():
    """A button object that can store a value and run a specefied
    function when it is clicked."""
    def __init__(self,
                 textObject: th.TextObject, 
                 function = None, # the function to run when this button is clicked
                 defaultFunctionArgs: List = [], # the args this buttons function is by default ran with
                 selectedColor = (255,0,0),
                 value: float = None, # a float stored inside a button. None if it doesnt store a value.
                 valueIncrement: float = 1, # How much the value changes when it is changed.
                 valueBounds: tuple[float,float] = (-10,10) # the min and max value of this button
                 ) -> None:
        """Initialize the button. Store the specefied values inside it."""

        self.textObject = textObject
        self.function = function
        """the function that is called when this button is clicked"""

        self.defaultFunctionArgs = defaultFunctionArgs

        self.value = value
        """a float stored inside a button. None if it doesnt store a value."""
        self.valueIncrement = valueIncrement
        """How much the value changes when it is changed."""
        self.valueBounds = valueBounds

        self.selectedColor = selectedColor
        self.notSelectedColor = textObject.color

    def Clicked(self):
        """Function that is called when this button is clicked."""
        if self.function != None:
            self.function(*self.defaultFunctionArgs) # run the passed in function
        print("Helo")

    def Selected(self):
        """Function that is run when this button is selected."""
        self.textObject.color = self.selectedColor
    def DeSelected(self):
        """Function that is run when this button is deselected."""
        self.textObject.color = self.notSelectedColor

    def ChangeValue(self,input: float) -> None:
        """Changes the value of this button and caps
        it att the min and max value of this button."""
        self.value += self.valueIncrement * input
        if self.valueBounds != None:
            if self.value > self.valueBounds[1]:
                self.value = self.valueBounds[1]
            elif self.value < self.valueBounds[0]:
                self.value = self.valueBounds[0]


class MenuGrid():
    """class that contains a number of buttons that can be 
    selected between and clicked, to run certain logic."""
    def __init__(self, 
                 mouseInputHandler: inputHandler.MouseInputHandler,
                 textHandler: th.TextHandler, 
                 buttons: list[list[Button]], # an arrray of all buttons contained in this menu grid
                 scrollCooldown: float = 0.2 # how long between when the player can change their selected button
                 ) -> None:
        """init the menugrid. store all values and create a 
        dictionary {position:button} to more easily access buttons."""
        
        self.mouseInputHandler = mouseInputHandler
        self.textHandler = textHandler

        self.buttons = buttons

        self.scrollCooldown = scrollCooldown
        self.currentScrollCooldown = scrollCooldown



        self.currentlySelectedPosition: tuple[int,int] = (0,0)
        """the currently selected position of this grid"""
        

        self.buttonsDict: dict[tuple[float,float] : Button] = {}
        """A dictionary where the keys are the grid
        position (x,y) of a button and the value
        is that button object."""

        

        # Fill the button dict
        for y,buttonRow in enumerate(self.buttons):
            for x,button in enumerate(buttonRow):
                self.buttonsDict[(x,y)] = button

        # run the selected function for the first selected button
        self.buttonsDict[self.currentlySelectedPosition].Selected()

        
    def RenderAllButtons(self):
        """Renders the text of all buttons in this
        MenuGrid."""
        for buttonRow in self.buttons:
            for button in buttonRow:
                self.textHandler.RenderTextobject(button.textObject)

    def CalculateNewPosition(self, input) -> tuple[float,float]:
        """Calculates and returns the new grid position
        from the players input."""
        newPos = ((self.currentlySelectedPosition[0] + input.x),(self.currentlySelectedPosition[1] + input.y))
        return newPos
    
    def HandleButtonInteractions(self):
        """Handles the players interaction with
        buttons. Can change the selected button,
        a buttons value and run their function if
        they were clicked."""
        selectedButton: Button = self.buttonsDict[self.currentlySelectedPosition] # get a reference to the currently selected button

        input = inputHandler.GetMoveInputVector()
        if (input.x != 0 or input.y != 0) and self.currentScrollCooldown <= 0: # if the player actually inputted something
            self.currentScrollCooldown = self.scrollCooldown # reset the scroll cooldown

            # change the value of a button if the player does horizontal input
            if selectedButton.value != None and input.x != 0:
                selectedButton.ChangeValue(input.x)
            else:
                # calculate the new selected position on the grid 
                newPos = self.CalculateNewPosition(input)

                if newPos in self.buttonsDict.keys(): # only move the cursor if the position youre trying to move it to exists
                    # deselect the currently selected button
                    selectedButton.DeSelected()
                    
                    
                    # move the cursor
                    self.currentlySelectedPosition = newPos

                    # select the currently selected bustton
                    selectedButton = self.buttonsDict[self.currentlySelectedPosition]
                    selectedButton.Selected()
                

        # handle the player clicking this frame
        mouseInput = self.mouseInputHandler.GetMouseInput()
        if mouseInput != None: # if the player clicked this frame
            selectedButton.Clicked()

    def Run(self):
        """Method that should be run every frame on this menu. 
        updates the position of the mousecursor 
        and checks if the player clicked any buttons."""
        
        self.currentScrollCooldown -= Time.deltaTime

        self.HandleButtonInteractions()

        self.RenderAllButtons()




    





                

        

# strings to refer to different menu states
mainMenuReference = "mainMenu"
playMenuReference = "playMenu"
instructionsReference = "instructions"
scoreboardReference = "scoreboard"


class Menu():
    """The games menus. Contains menu grids with buttons
    and renders different menu text depending on what menu
    the player is in."""
    def __init__(self, 
                 displaySurface: pg.surface,
                 menuMode: str = mainMenuReference) -> None:
        """Initialize the menu. Create all the text
        and the menu grids."""
                 
                 

        self.displaySurface = displaySurface

        self.menuMode = menuMode
        """Which mode the menu is currently in, which submenu it is in"""

        self.mouseInputHandler = inputHandler.MouseInputHandler()

         
        self.gameRunning = False 
        """If the game should start. Set to true when the game is signaled by this class to start."""

        # Create a texthandler that can render text from a string reference
        self.textHandler = th.TextHandler(self.displaySurface,
                                          {
                                              # This dict is really usefull for static text
                                              "title":th.TextObject(mainFont,60,(255,255,255),"Memory3D",(300,150)),
                                              "byMe":th.TextObject(mainFont,30,(255,255,255),"By Isac Zobec ! !!!",(300,200)),
                                              "splashText":th.TextObject(mainFont,30,(255,255,255),"Memory3D Extra low fps edition",(300,250)),

                                              "instructions1":th.TextObject(mainFont,40,(255,255,255),"... you dont know what memory is...?",(50,280)),
                                              "instructions2":th.TextObject(mainFont,20,(255,255,255),"Uhhh.. ok. The goal of memory is to match all the cards. Every card has a matching other card that matches the previous card.",(50,350)),
                                              "instructions3":th.TextObject(mainFont,20,(255,255,255),"Alas, every card has a pair you have to find. Every turn, you get to turn up two cards. If you find the matching pair,",(50,400)),
                                              "instructions4":th.TextObject(mainFont,20,(255,255,255),"The cards stay up the next turn and you have succesfully found them. Once this has happened with all cards, you win.",(50,450)),
                                              "instructions5":th.TextObject(mainFont,20,(255,255,255),"For extra replay value, you can try to increase your score by finding all cards faster or in less turns.",(50,500)),
                                              "instructions6":th.TextObject(mainFont,20,(255,255,255),"... but that sounds really boring. you can also go outside and touch some grass.",(50,550)),
                                            
                                              

                                              

                                          }
                                          )
        
        # Create the buttons and text of all the different menus:

        # Main menu
        
        playText = th.TextObject(mainFont,60,(255,255,255),"Play",(300,400))
        scoreBoardText = th.TextObject(mainFont,60,(255,255,255),"Scoreboard",(500,400))
        exitText = th.TextObject(mainFont,60,(255,255,255),"Exit",(300,500))
        instructionsText = th.TextObject(mainFont,60,(255,255,255),"Instructions",(500,500))

        self.startMenuButtons = [[Button(playText,self.SetMenuMode,[playMenuReference]),Button(scoreBoardText,self.SetMenuMode,[scoreboardReference])],
                                 [Button(exitText,self.ExitGame),Button(instructionsText,self.SetMenuMode,[instructionsReference])]]
        
        self.mainMenuGrid = MenuGrid(self.mouseInputHandler,self.textHandler,self.startMenuButtons)

        # Instructions menu

        self.instructionsExitText = th.TextObject(mainFont,60,(255,255,255),"Exit to main menu",(75,75))
        self.instructionsMenuButtons = [[Button(self.instructionsExitText,self.SetMenuMode,[mainMenuReference])]]

        self.instructionsMenuGrid = MenuGrid(self.mouseInputHandler,self.textHandler,self.instructionsMenuButtons)


        # Play menu

        self.boardSizeXText: th.TextObject = th.TextObject(mainFont,40,(255,255,255),"Board columns: <a/d>",(50,50))
        self.boardSizeXValueText = th.TextObject(mainFont,40,(255,255,255),str(gameSettings.boardSize[0]),(500,50))
        self.boardSizeYText = th.TextObject(mainFont,40,(255,255,255),"Board rows: <a/d>",(50,100))
        self.boardSizeYValueText = th.TextObject(mainFont,40,(255,255,255),str(gameSettings.boardSize[1]),(500,100))
        self.boardSizeZText = th.TextObject(mainFont,40,(255,255,255),"Board depth: <a/d>",(590,100))
        self.boardSizeZValueText = th.TextObject(mainFont,40,(255,255,255),str(gameSettings.boardSize[1]),(950,100))
        
        self.minWordLengthText = th.TextObject(mainFont,40,(255,255,255),"Min word length: <a/d>",(50,150))
        self.minWordLengthValueText = th.TextObject(mainFont,40,(255,255,255),str(gameSettings.boardSize[1]),(500,150))
        self.maxWordLengthText = th.TextObject(mainFont,40,(255,255,255),"Max word length: <a/d>",(50,200))
        self.maxWordLengthValueText = th.TextObject(mainFont,40,(255,255,255),str(gameSettings.boardSize[1]),(500,200))
    
        self.playButtonText = th.TextObject(mainFont,60,(255,255,255),"PLAY!",(50,320))

        self.playExitText = th.TextObject(mainFont,60,(255,255,255),"Exit to main menu",(50,400))


        self.playMenuButtons = [[Button(self.boardSizeXText,value=gameSettings.boardSize[0],valueBounds=(2,10))],
                                [Button(self.boardSizeYText,value=gameSettings.boardSize[1],valueBounds=(2,10),valueIncrement=2)], # valueincrement = 2 so that there isnt any risk of there being an uneven amount of cards
                                [Button(self.boardSizeZText,value=gameSettings.boardSize[2],valueBounds=(2,10))],
                                [Button(self.minWordLengthText,value=3,valueBounds=(1,3),valueIncrement=1)], 
                                [Button(self.maxWordLengthText,value=3,valueBounds=(3,8),valueIncrement=1)], 
                                [Button(self.playButtonText,selectedColor=(0,255,0),function=self.StartGame)],
                                [Button(self.playExitText,self.SetMenuMode,[mainMenuReference])],
                                 ]

        self.playMenuGrid = MenuGrid(self.mouseInputHandler,self.textHandler,self.playMenuButtons)

        # scoreBoard

        self.scoreBoardExitText = th.TextObject(mainFont,30,(255,255,255),"Exit to main menu",(75,600))
        self.scoreBoardMenuButtons = [[Button(self.scoreBoardExitText,self.SetMenuMode,[mainMenuReference])]]

        self.scoreBoardMenuGrid = MenuGrid(self.mouseInputHandler,self.textHandler,self.scoreBoardMenuButtons)

        self.UpdateScoreBoardMenu()
        

    def UpdateScoreBoardMenu(self) -> None:
        """Gets and stores a list of all scoreboard entries."""
        self.scoreBoardEntries = self.textHandler.GetTextObjectsFromDicts(scoreBoard.GetScoreBoardEntries())
        
                                 
        
    def SetMenuMode(self, menuMode: str) -> None:
        """Sets the menumode to the given menu mode."""
        self.menuMode = menuMode

        if self.menuMode == scoreboardReference:
            self.UpdateScoreBoardMenu()

    def ExitGame(self) -> None:
        """Safely closes the application."""
        pg.quit()
        sys.exit()

    def StartGame(self) -> None:
        """Starts the active memory game."""

        gameSettings.boardSize = (int(self.playMenuButtons[0][0].value),int(self.playMenuButtons[1][0].value),int(self.playMenuButtons[2][0].value)) # update the board size
        gameSettings.minMaxWordLength = (int(self.playMenuButtons[3][0].value),int(self.playMenuButtons[4][0].value)) # update the board size
        self.gameRunning = True # sends a signal to start the game


    def Run(self) -> None:
        """Method that should be ran every frame the menu is active.
        renders the text of the current menu and updates it."""
        
        if self.menuMode == mainMenuReference:

            self.textHandler.RenderText("title")
            self.textHandler.RenderText("byMe")
            self.textHandler.RenderText("splashText")

            self.mainMenuGrid.Run()

        elif self.menuMode == instructionsReference:

            self.textHandler.RenderText("instructions1")
            self.textHandler.RenderText("instructions2")
            self.textHandler.RenderText("instructions3")
            self.textHandler.RenderText("instructions4")
            self.textHandler.RenderText("instructions5")
            self.textHandler.RenderText("instructions6")

            self.instructionsMenuGrid.Run()
        
        elif self.menuMode == playMenuReference:

            self.playMenuGrid.Run()

            self.boardSizeXValueText.text = str(self.playMenuButtons[0][0].value)
            self.boardSizeYValueText.text = str(self.playMenuButtons[1][0].value)
            self.boardSizeZValueText.text = str(self.playMenuButtons[2][0].value)

            self.minWordLengthValueText.text = str(self.playMenuButtons[3][0].value)
            self.maxWordLengthValueText.text = str(self.playMenuButtons[4][0].value)

            self.textHandler.RenderTextobject(self.boardSizeXValueText)
            self.textHandler.RenderTextobject(self.boardSizeYValueText)
            self.textHandler.RenderTextobject(self.boardSizeZValueText)
            self.textHandler.RenderTextobject(self.maxWordLengthValueText)
            self.textHandler.RenderTextobject(self.minWordLengthValueText)

        elif self.menuMode == scoreboardReference:

            self.scoreBoardMenuGrid.Run()

            # render all scoreboard entries
            for entryTextObject in self.scoreBoardEntries:
                self.textHandler.RenderTextobject(entryTextObject)


    



