from typing import List
from Objects3D import Face
import renderer as r
import Objects3D as obj
import numpy as np
from numpy import array as ar
import Time
import image

imageCard = "imageCard"
textCard = "textCard"

class memoryCard(obj.R3Object):
    def __init__(self, 
                 game, # the game class this card belongs to 
                 gridPos: List[int], # the position of this memory card on the board
                 cardType: str = imageCard, # if this card has an image or text on its upside
                 planeImageName: str = None) -> None: # the name of the image if this card is an imageCard
        
        self.game = game
        self.gridPos = gridPos
        self.cardType = cardType
        self.planeImageName = planeImageName

        if cardType == imageCard:

            super().__init__([obj.Face(         [
                                                obj.Vertex(ar([-1.364,1,0,1])),
                                                obj.Vertex(ar([-1.364,-1,0,1])),
                                                obj.Vertex(ar([1.364,-1,0,1])),
                                                obj.Vertex(ar([1.364,1,0,1])),
                                                ],
                                                virtualCamera=self.game.renderer.camera,
                                                planeImage="cardBackside",
                                                planeImageScale=95)],
                                                position=ar([5,1,0,1]),
                                                
                                                triangulate=False)

        