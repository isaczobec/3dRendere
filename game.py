import renderer as r
import Objects3D as obj
import numpy as np
from numpy import array as ar
import Time
from memoryCard import MemoryCard
import memoryCard as mc
import gameSettings
from typing import List
import fileHandling
import random
import pygame as pg
from inputHandler import MouseInputHandler
import texthandling
import scoreBoard


baseScore: int = 2000
"""The score the player gets if their time * guesses = 1"""


class GameManager():
    def __init__(self,
                 rendererObject: r.Renderer,
                 displaySurface: pg.Surface,
                 ) -> None:
        self.renderer: r.Renderer = rendererObject

        self.memoryCardList: List[MemoryCard] = []
        """List that contains all memorycards in this game."""

        self.fullWordList = fileHandling.GetWordList()
        self.CreateBoard()

        self.displaySurface = displaySurface # the displaySurface used to render the game


        self.selectedCards: List[MemoryCard] = []
        """which cards are curently selected by the player. Maximum length of 2."""

        self.timeUntilTurnBackCards: float = 0
        self.currentlyWaitingToTurnBackCards: bool = False

        self.cardsRemaining: int = gameSettings.boardSize[0] * gameSettings.boardSize[1]

        self.guesses: int = 0
        """How many cards the player has turned."""

        self.startTime = Time.passedTime

        self.gameFinnished: bool = False # if the player has won the game
        self.returnToMenu: bool = False # set to true when the player should return to the menu

        self.textManager = texthandling.WonTextManager(self.displaySurface) # initialize the texthandler

        self.mouseInputHandler = MouseInputHandler() # used to check if the player clicks to exit the game after they have won


        
        

        




    def CreateBoard(self):
        """Creates memory cards in a grid."""

        wordLengthRange = range(gameSettings.minMaxWordLength[0],gameSettings.minMaxWordLength[1] + 1)
        alphabet = [chr(v) for v in range(ord('a'), ord('a') + 26)] # generate a list of the alphabet

        wordList = []
        amountOfWordsToChoose = int(gameSettings.boardSize[0] * gameSettings.boardSize[1] / 2)
        for i in range(amountOfWordsToChoose):


            originalWord = random.choice(self.fullWordList)


            # give the word a random length
            choosenWord = originalWord
            wordLength = random.choice(wordLengthRange)
            while choosenWord.__len__() < wordLength:
                choosenWord = choosenWord + random.choice(alphabet)
            if choosenWord.__len__() > wordLength:
                choosenWord = choosenWord[:wordLength]

            # Append the word twice so that it will belong to two cards
            wordList.append(choosenWord)
            wordList.append(choosenWord)
            self.fullWordList.remove(originalWord)
            

        for x in range(gameSettings.boardSize[0]):
            for y in range(gameSettings.boardSize[1]):
                memoryCard = MemoryCard(self,(x,y),virtualCamera = self.renderer.camera,cardType=mc.textCard,cardText=wordList.pop(random.randrange(0,len(wordList))))
                self.memoryCardList.append(memoryCard)
                self.renderer.objectList.append(memoryCard)

    

    def run(self):
        """Runs every frame. Lets the player turn up cards and handles turning them back."""
        
        if self.gameFinnished: # if the player has won the game
            self.textManager.RenderEndgameText()

            self.textManager.RenderText("placementText")
            self.textManager.RenderText("scoreBoardMenuText")

            if self.mouseInputHandler.GetMouseInput() != None:
                self.returnToMenu = True
        
        if self.renderer.clickedObject != None: # if the player clicked an object this frame
            self.renderer.clickedObject.ObjectClicked()

            if len(self.selectedCards) == 2:

                if self.selectedCards[0].cardType == mc.textCard and self.selectedCards[1].cardType == mc.textCard:
                    if self.selectedCards[0].cardText == self.selectedCards[1].cardText:
                        self.FoundCards()
                        
                elif self.selectedCards[0].cardType == mc.imageCard and self.selectedCards[1].cardType == mc.imageCard:
                    if self.selectedCards[0].planeImageName == self.selectedCards[1].planeImageName:
                        self.FoundCards()

            
        if len(self.selectedCards) == 2 and self.currentlyWaitingToTurnBackCards == False: # check if the player has turned up 2 cards without a matching pair, then start turning them back
            self.timeUntilTurnBackCards = gameSettings.cardsTurnBackCooldown
            self.currentlyWaitingToTurnBackCards = True

        self.HandleCardTurnBack()


        for obj in self.renderer.objectList: # update every object
            obj.Update()


            


    

    def FoundCards(self) -> None:
        """Function that should be executed when the player finds two cards."""
        for card in self.selectedCards:
            card.found = True
        self.selectedCards.clear() # clear the list of selected cards as they have been found

        self.cardsRemaining -= 2

        if self.cardsRemaining <= 0:
            self.FinishGame()


    def FinishGame(self) -> None:
        """Ran once the player wins the game. Calculates the score and creates text for the players placement."""

        # Calculate the score
        self.gameFinnished = True
        totalTime: float = Time.passedTime - self.startTime
        score = self.CalculateTotalScore(self.guesses,totalTime)
        self.textManager.CreateStatText(totalTime,self.guesses,score)

        # create the placement text
        placeMentText = ""
        scoreBoardEntries = scoreBoard.GetScoreBoardEntries()
        for index,entry in enumerate(scoreBoardEntries):
            if float(entry["score"]) < score:
                placeMentText = f"you placed {index+1} out of {len(scoreBoardEntries)} people who have played before you!"
                break

        scoreBoard.AddScoreBoardEntry(score=score,time = totalTime,moves=self.guesses)

        self.textManager.CreateTextObject("placementText","Comic Sans",30,(255,255,255),placeMentText,defaultPosition=(50,500))
        self.textManager.CreateTextObject("scoreBoardMenuText","Comic Sans",20,(255,255,255),"You can view highscores in the scoreboard menu!",defaultPosition=(50,550))
        
 
        
        


    def HandleCardTurnBack(self) -> None:

        # if the cards should be turned back this frame
        if self.timeUntilTurnBackCards <= 0 and self.currentlyWaitingToTurnBackCards == True:
            for card in self.selectedCards:
                card.StartFlip()
            self.currentlyWaitingToTurnBackCards = False
            self.selectedCards.clear() # clear the selected cards list
        else:
            self.timeUntilTurnBackCards -= Time.deltaTime





    def __deepcopy__(self,memo): # override the deepcopy method to not copy this class. 
        return self
    

    def CalculateTotalScore(self, time: float, guesses: int) -> None:
        """Calculates the players total score."""
        return round(baseScore/(time * guesses),1)
            

