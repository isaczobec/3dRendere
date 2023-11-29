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

from texthandling import TextManager

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

        self.gameFinnished: bool = False

        self.textManager = TextManager(self.displaySurface) # initialize the texthandler

        
        

        




    def CreateBoard(self):
        """Creates memory cards in a grid."""

        fullWordList = fileHandling.GetWordList()

        wordList = []
        amountOfWordsToChoose = int(gameSettings.boardSize[0] * gameSettings.boardSize[1] / 2)
        for i in range(amountOfWordsToChoose):
            choosenWord = random.choice(fullWordList)
            # Append the word twice so that it will belong to two cards
            wordList.append(choosenWord)
            wordList.append(choosenWord)
            fullWordList.remove(choosenWord)
            

        for x in range(gameSettings.boardSize[0]):
            for y in range(gameSettings.boardSize[1]):
                memoryCard = MemoryCard(self,(x,y),virtualCamera = self.renderer.camera,cardType=mc.textCard,cardText=wordList.pop(random.randrange(0,len(wordList))))
                self.memoryCardList.append(memoryCard)
                self.renderer.objectList.append(memoryCard)

    

    def run(self):
        """Runs every frame. Lets the player turn up cards and handles turning them back."""
        
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


        if self.gameFinnished: # if the player has won the game
            self.textManager.RenderEndgameText()
    

    def FoundCards(self) -> None:
        """Function that should be executed when the player finds two cards."""
        for card in self.selectedCards:
            card.found = True
        self.selectedCards.clear() # clear the list of selected cards as they have been found

        self.cardsRemaining -= 2

        if self.cardsRemaining <= 0:
            self.FinishGame()


    def FinishGame(self) -> None:

        self.gameFinnished = True

        totalTime: float = Time.passedTime - self.startTime
        self.textManager.CreateStatText(totalTime,self.guesses,self.CalculateTotalScore(self.guesses,totalTime))
 
        
        


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
            

