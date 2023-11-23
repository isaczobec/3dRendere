import renderer as r
import Objects3D as obj
import numpy as np
from numpy import array as ar
import Time
from memoryCard import MemoryCard
import memoryCard as mc
import gameSettings
from typing import List


class GameManager():
    def __init__(self,rendererObject: r.Renderer) -> None:
        self.renderer: r.Renderer = rendererObject

        self.memoryCardList: List[MemoryCard] = []
        """List that contains all memorycards in this game."""

        self.CreateBoard()



    def CreateBoard(self):
        """Creates memory cards in a grid."""

        for x in range(gameSettings.boardSize[0]):
            for y in range(gameSettings.boardSize[1]):
                memoryCard = MemoryCard((x,y),virtualCamera = self.renderer.camera,cardType=mc.textCard,cardText="hej")
                self.memoryCardList.append(memoryCard)
                self.renderer.objectList.append(memoryCard)


    def run(self):
        
        if self.renderer.clickedObject != None:
            self.renderer.clickedObject.ObjectClicked()
            

            #self.renderer.clickedObject.Rotate(70*Time.deltaTime,0,0)

        for obj in self.renderer.objectList: # update every object
            obj.Update()
            

