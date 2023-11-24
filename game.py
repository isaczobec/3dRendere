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

class GameManager():
    def __init__(self,rendererObject: r.Renderer) -> None:
        self.renderer: r.Renderer = rendererObject

        self.memoryCardList: List[MemoryCard] = []
        """List that contains all memorycards in this game."""

        self.CreateBoard()


        self.selectedCards: List[MemoryCard] = []
        """which cards are curently selected by the player. Maximum length of 2."""

        self.timeUntilTurnBackCards: float = 0
        self.currentlyWaitingToTurnBackCards: bool = False






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
                        print("found")
                elif self.selectedCards[0].cardType == mc.imageCard and self.selectedCards[1].cardType == mc.imageCard:
                    if self.selectedCards[0].planeImageName == self.selectedCards[1].planeImageName:
                        self.FoundCards()
                        print("found")

            
        if len(self.selectedCards) == 2 and self.currentlyWaitingToTurnBackCards == False: # check if the player has turned up 2 cards without a matching pair, then start turning them back
            self.timeUntilTurnBackCards = gameSettings.cardsTurnBackCooldown
            self.currentlyWaitingToTurnBackCards = True

        self.HandleCardTurnBack()
            

            


        for obj in self.renderer.objectList: # update every object
            obj.Update()

    def FoundCards(self):
        """Function that should be executed when the player finds two cards."""
        for card in self.selectedCards:
            card.found = True
        self.selectedCards.clear() # clear the list of selected cards as they have been found

    def HandleCardTurnBack(self):

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
            

