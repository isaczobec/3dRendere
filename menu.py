import pygame as pg
import texthandling as th
import inputHandler
from typing import List
import sys
import gameSettings


mainFont = "Comic Sans"


class Button():
    def __init__(self,
                 textObject: th.TextObject, 
                 function = None, # the function to run when this button is clicked
                 defaultFunctionArgs: List = [],
                 selectedColor = (255,0,0),
                 value: float = None, # a float stored inside a button. None if it doesnt store a value.
                 valueIncrement: float = 1, # How much the value changes when it is changed.
                 valueBounds: tuple[float,float] = (-10,10) # the min and max value of this button
                 ) -> None:

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


class MenuGrid():
    def __init__(self, mouseInputHandler: inputHandler.MouseInputHandler,textHandler: th.TextHandler, buttons: List[List[Button]]) -> None:
        
        self.mouseInputHandler = mouseInputHandler
        self.textHandler = textHandler

        self.buttons = buttons

        

        self.buttonsDict: dict[tuple[float,float] : Button] = {}


        self.currentlySelectedPosition: tuple[int,int] = (0,0)
        """the currently selected position of this grid"""
        

        for y,buttonRow in enumerate(self.buttons):
            for x,button in enumerate(buttonRow):
                self.buttonsDict[(x,y)] = button
                print(button)

        self.buttonsDict[self.currentlySelectedPosition].Selected()


        print("buttonsdict",self.buttonsDict)
        
    def RenderAllButtons(self):
        for buttonRow in self.buttons:
            for button in buttonRow:
                self.textHandler.RenderTextobject(button.textObject)

    def Run(self):
        """Method that should be run every frame on this menu. updates the position of the mousecursor and checks if the player clicked any buttons."""
        

        selectedButton: Button = self.buttonsDict[self.currentlySelectedPosition] # get a reference to the currently selected

        input = inputHandler.GetMoveInputVector()
        if input.x != 0 or input.y != 0: # if the player actually inputted something

            # change the value of a button if the player does vertical input
            if selectedButton.value != None and input.x != 0:
                selectedButton.value += selectedButton.valueIncrement * input.x
                if selectedButton.valueBounds != None:
                    if selectedButton.value > selectedButton.valueBounds[1]:
                        selectedButton.value = selectedButton.valueBounds[1]
                    elif selectedButton.value < selectedButton.valueBounds[0]:
                        selectedButton.value = selectedButton.valueBounds[0]
            else:
                newPos = ((self.currentlySelectedPosition[0] + input.x),(self.currentlySelectedPosition[1] + input.y))

                if newPos in self.buttonsDict.keys(): # only move the cursor if the position youre trying to move it to exists

                    # deselect the currently selected button
                    selectedButton.DeSelected()
                    
                    
                    # move the cursor
                    self.currentlySelectedPosition = newPos

                    # select the currently selected button
                    selectedButton = self.buttonsDict[self.currentlySelectedPosition]
                    selectedButton.Selected()
                

        # handle the player clicking this frame
        mouseInput = self.mouseInputHandler.GetMouseInput()
        print(mouseInput)
        if mouseInput != None: # if the player clicked this frame
            print("yes")
            selectedButton.Clicked()

        self.RenderAllButtons()


    





                

        


mainMenuReference = "mainMenu"
playMenuReference = "playMenu"
instructionsReference = "instructions"
scoreboardReference = "scoreboard"


class Menu():
    def __init__(self, 
                 displaySurface: pg.surface,
                 menuMode: str = mainMenuReference) -> None:
                 
                 

        self.displaySurface = displaySurface

        self.menuMode = menuMode
        """Which mode the menu is currently in, which submenu it is in"""

        self.mouseInputHandler = inputHandler.MouseInputHandler()

         

        
        self.textHandler = th.TextHandler(self.displaySurface,
                                          {
                                              # This dict is really usefull for static text
                                              "title":th.TextObject(mainFont,60,(255,255,255),"Memory3D",(300,150)),
                                              "byMe":th.TextObject(mainFont,30,(255,255,255),"By Isac Zobec ! !!!",(300,200)),
                                              "splashText":th.TextObject(mainFont,30,(255,255,255),"Memory3D Extra low fps edition",(300,250)),

                                              "instructions1":th.TextObject(mainFont,40,(255,255,255),"... you dont know what memory is...?",(50,280)),
                                              "instructions2":th.TextObject(mainFont,20,(255,255,255),"The goal of memory is to match all the cards. Every card has a matching other card that matches the previous card.",(50,350)),
                                              "instructions3":th.TextObject(mainFont,20,(255,255,255),"Alas, every card has a pair you have to find. Every turn, you get to turn up two cards. If you find the matching pair,",(50,400)),
                                              "instructions4":th.TextObject(mainFont,20,(255,255,255),"The cards stay up the next turn and you have succesfully found them. Once this has happened with all cards, you win.",(50,450)),
                                              "instructions5":th.TextObject(mainFont,20,(255,255,255),"For extra replay value, you can try to increase your score by finding all cards faster or in less turns.",(50,500)),
                                              "instructions6":th.TextObject(mainFont,20,(255,255,255),"Or you can go outside and touch some grass. I dont make the rules. And i certainly do not touch grass.",(50,550)),
                                              "instructions7":th.TextObject(mainFont,20,(255,255,255),"That's for certain.",(50,600)),
                                            
                                              

                                              

                                          }
                                          )
        
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

        self.boardSizeXText: th.TextObject = th.TextObject(mainFont,30,(255,255,255),"Board columns:",(50,50))
        self.boardSizeXValueText = th.TextObject(mainFont,30,(255,255,255),str(gameSettings.boardSize[0]),(200,50))
        self.boardSizeYText = th.TextObject(mainFont,30,(255,255,255),"Board rows:",(50,100))
        self.boardSizeYValueText = th.TextObject(mainFont,30,(255,255,255),str(gameSettings.boardSize[1]),(200,100))
    
        self.playMenuButtons = [[Button(self.boardSizeXText,value=gameSettings.boardSize[0],valueBounds=(2,10))],
                                [Button(self.boardSizeYText,value=gameSettings.boardSize[1],valueBounds=(2,10),valueIncrement=2)], # valueincrement = 2 so that there isnt any risk of there being an uneven amount of cards
                                 ]

        self.playMenuGrid = MenuGrid(self.mouseInputHandler,self.textHandler,self.playMenuButtons)
        
    
        


                                 
        
    def SetMenuMode(self, menuMode: str):
        """Sets the menumode to the given menu mode."""
        self.menuMode = menuMode

    def ExitGame(self):
        """Safely closes the application."""
        pg.quit()
        sys.exit()


    def Run(self):
        """Method that should be ran every frame the menu is active."""
        
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
            self.textHandler.RenderText("instructions7")

            self.instructionsMenuGrid.Run()
        
        elif self.menuMode == playMenuReference:

            self.playMenuGrid.Run()

            self.boardSizeXValueText.text = str(self.playMenuButtons[0][0].value)
            self.boardSizeYValueText.text = str(self.playMenuButtons[1][0].value)

            self.textHandler.RenderTextobject(self.boardSizeXValueText)
            self.textHandler.RenderTextobject(self.boardSizeYValueText)


    



