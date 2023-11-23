from typing import List
from Objects3D import Face
import renderer as r
import Objects3D as obj
import numpy as np
from numpy import array as ar
from math import pi
import Time
import image
import gameSettings
import copy
import virtualCamera

imageCard = "imageCard"
textCard = "textCard"

class MemoryCard(obj.R3Object):
    """Class that extends the r3object class (because it is a 3d object) and that contains logic for flipping, matching with other cards, etc."""

    def __init__(self, 
                 gridPos: tuple[int], # the position of this memory card on the board
                 virtualCamera: virtualCamera.VirtualCamera, # the camera used to render this object
                 cardType: str = imageCard, # if this card has an image or text on its upside
                 planeImageName: str = None, # the name of the image if this card is an imageCard
                 cardText: str = None) -> None: # the text displayed on this card if it is a textcard
        
        self.gridPos = gridPos
        self.cardType = cardType

        self.isTurning = False
        """If this card is currently being animated to turn around"""
        self.degreesTurned = 0
        """How many degrees this card has currently been turned in the turn animation."""

        cardDim = gameSettings.cardDimensionRatio

        if cardType == imageCard:

            super().__init__(                   [obj.Face([
                                                obj.Vertex(ar([-cardDim[0],0,cardDim[1],1])),
                                                obj.Vertex(ar([-cardDim[0],0,-cardDim[1],1])),
                                                obj.Vertex(ar([cardDim[0],0,-cardDim[1],1])),
                                                obj.Vertex(ar([cardDim[0],0,cardDim[1],1])),
                                                ],
                                                virtualCamera=virtualCamera,
                                                planeImage="cardBackside",
                                                planeImageScale=(95,95)),
                                                obj.Face([
                                                obj.Vertex(ar([-cardDim[0],-0.01,cardDim[1],1])),
                                                obj.Vertex(ar([-cardDim[0],-0.01,-cardDim[1],1])),
                                                obj.Vertex(ar([cardDim[0],-0.01,-cardDim[1],1])),
                                                obj.Vertex(ar([cardDim[0],-0.01,cardDim[1],1])),
                                                ],
                                                virtualCamera=virtualCamera,
                                                planeImage=planeImageName,
                                                planeImageScale=(95,95))],
                                                position=ar([self.gridPos[0]*gameSettings.cardOffset[0],-4,self.gridPos[1]*gameSettings.cardOffset[1],1]), # make sure this cards world position is consistent with its grid position
                                                
                                                
                                                triangulate=False)
            
        if cardType == textCard:

            letterFaceList = []

            wordLength = len(cardText)
            step = cardDim[0]/wordLength



            for i,c in enumerate(cardText):

                xLoc1 = -cardDim[0] + step * (i)*2
                xLoc2 = -cardDim[0] + step * (i+1)*2

                letterFaceList.append(obj.Face([
                                                obj.Vertex(ar([xLoc1,-0,cardDim[1],1])),
                                                obj.Vertex(ar([xLoc1,-0,-cardDim[1],1])),
                                                obj.Vertex(ar([xLoc2,-0,-cardDim[1],1])),
                                                obj.Vertex(ar([xLoc2,-0,cardDim[1],1])),
                                                ],
                                                virtualCamera=virtualCamera,
                                                planeImage=c,
                                                planeImageScale=(95,95*wordLength),
                                                ),
                                                )
                
            # Add the backside of the card
            letterFaceList.append(obj.Face([ 
                                                obj.Vertex(ar([-cardDim[0],0.5,cardDim[1],1])),
                                                obj.Vertex(ar([-cardDim[0],0.5,-cardDim[1],1])),
                                                obj.Vertex(ar([cardDim[0],0.5,-cardDim[1],1])),
                                                obj.Vertex(ar([cardDim[0],0.5,cardDim[1],1])),
                                                ],
                                                virtualCamera=virtualCamera,
                                                planeImage="cardBackside",
                                                planeImageScale=(95,95)))
            
            super().__init__(letterFaceList,
                             position=ar([self.gridPos[0]*gameSettings.cardOffset[0],-4,self.gridPos[1]*gameSettings.cardOffset[1],1]), # make sure this cards world position is consistent with its grid position
                             triangulate=False)


            
    def StartFlip(self) -> None:
        """Start the turn animation of this card."""

        if not self.isTurning:
            self.degreesTurned = 0
            self.isTurning = True


    def AnimateFlip(self,turnSpeed = gameSettings.flipCardSpeed):
        """Update the flip animation. Called every frame."""

        if self.degreesTurned <= 180:
            ang = turnSpeed*Time.deltaTime
            self.Rotate(ang,0,0)
            self.degreesTurned += ang

        else:

            self.Rotate(180-self.degreesTurned,0,0) # rotate the card back so it doesnt overturn
            self.degreesTurned = 0
            self.isTurning = False

    def Update(self):
        if self.isTurning:
            self.AnimateFlip()

    def ObjectClicked(self):
        self.StartFlip()

            


        