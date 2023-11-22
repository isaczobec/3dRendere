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
    def __init__(self, 
                 gridPos: tuple[int], # the position of this memory card on the board
                 virtualCamera: virtualCamera.VirtualCamera, # the camera used to render this object
                 cardType: str = imageCard, # if this card has an image or text on its upside
                 planeImageName: str = None) -> None: # the name of the image if this card is an imageCard
        
        self.gridPos = gridPos
        self.cardType = cardType
        self.planeImageName = planeImageName

        self.isTurning = False
        """If this card is currently being animated to turn around"""
        self.degreesTurned = 0
        """How many degrees this card has currently been turned in the turn animation."""

        if cardType == imageCard:

            super().__init__(                   [obj.Face([
                                                obj.Vertex(ar([-1.364,0,1,1])),
                                                obj.Vertex(ar([-1.364,0,-1,1])),
                                                obj.Vertex(ar([1.364,0,-1,1])),
                                                obj.Vertex(ar([1.364,0,1,1])),
                                                ],
                                                virtualCamera=virtualCamera,
                                                planeImage="cardBackside",
                                                planeImageScale=95),
                                                obj.Face([
                                                obj.Vertex(ar([-1.364,0.01,1,1])),
                                                obj.Vertex(ar([-1.364,0.01,-1,1])),
                                                obj.Vertex(ar([1.364,0.01,-1,1])),
                                                obj.Vertex(ar([1.364,0.01,1,1])),
                                                ],
                                                virtualCamera=virtualCamera,
                                                planeImage="cat",
                                                planeImageScale=95)],
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

            


        