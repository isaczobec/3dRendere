"""Module containing the memorycard class."""

import Objects3D as obj
from numpy import array as ar
import Time
import gameSettings
import virtualCamera

# Reference strings for different card types
imageCard = "imageCard"
textCard = "textCard"

# the reference string for the card backside image
cardBacksideStr = "cardBackside"

class MemoryCard(obj.R3Object):
    """Class representing a memory card.
    extends the r3object class (because it is a 3d object) 
    and  contains logic for flipping, 
    matching with other cards, etc."""

    def __init__(self, 
                 game, # the game class this card belongs to
                 gridPos: tuple[int,int], # the position of this memory card on the board
                 virtualCamera: virtualCamera.VirtualCamera, # the camera used to render this object
                 cardType: str = imageCard, # if this card has an image or text on its upside
                 planeImageName: str = None, # the name of the image if this card is an imageCard
                 cardText: str = None,# the text displayed on this card if it is a textcard
                 turnedUp: bool = False) -> None: 
        """Initialize the card. Store a reference to its content
        string and initialize the parent class to create 3d planes with
        the correct images for this card."""
        
        self.gridPos = gridPos
        """Which position on the board grid this card is at."""

        self.cardType = cardType
        
        self.game = game # a reference to the gamemanager class this card is stored in.

        self.isTurning = False
        """If this card is currently being animated to turn around"""
        self.degreesTurned = 0
        """How many degrees this card has currently been turned in the turn animation."""

        self.planeImageName = planeImageName
        self.cardText = cardText

        cardDim = gameSettings.cardDimensionRatio
        
        backScale = gameSettings.cardBackSizeScaleFactor

        self.found = False
        """if this memorycard has been found."""

        self.turnedUp = turnedUp
        """if this card is currently turned up."""


        # Init the parent class (3d object) to create a 3d plane with this cards images.
        if cardType == imageCard:

            super().__init__(                   [obj.Face([
                                                obj.Vertex(ar([-cardDim[0]*backScale,0,cardDim[1]*backScale,1])),
                                                obj.Vertex(ar([-cardDim[0]*backScale,0,-cardDim[1]*backScale,1])),
                                                obj.Vertex(ar([cardDim[0]*backScale,0,-cardDim[1]*backScale,1])),
                                                obj.Vertex(ar([cardDim[0]*backScale,0,cardDim[1]*backScale,1])),
                                                ],
                                                virtualCamera=virtualCamera,
                                                planeImage=cardBacksideStr,
                                                planeImageScale=(95,95)),
                                                obj.Face([
                                                obj.Vertex(ar([-cardDim[0],-0.01,cardDim[1],1])),
                                                obj.Vertex(ar([-cardDim[0],-0.01,-cardDim[1],1])),
                                                obj.Vertex(ar([cardDim[0],-0.01,-cardDim[1],1])),
                                                obj.Vertex(ar([cardDim[0],-0.01,cardDim[1],1])),
                                                ],
                                                virtualCamera=virtualCamera,
                                                planeImage=planeImageName,
                                                planeImageScale=(95,95),
                                                flipNormal=True)],
                                                position=ar([self.gridPos[0]*gameSettings.cardOffset[0],-9,self.gridPos[1]*gameSettings.cardOffset[1],1]), # make sure this cards world position is consistent with its grid position
                                                
                                                
                                                triangulate=False)
            
        # Init the parent class (3d object) to create a 3d plane with this cards letter images.
        if cardType == textCard:

            # create and fill a list with planes that have images of the letters of this card
            letterFaceList = []

            wordLength = len(cardText)
            step = cardDim[0]/wordLength

            # create faces for all letters
            for i,c in enumerate(cardText):

                # calculate x position of every letter plane
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
                                                planeImageScale=(1,wordLength/3),
                                                enabled=False,
                                                flipNormal=True
                                                ),
                                                )
                
            # Add the backside of the card
            letterFaceList.append(obj.Face([ 
                                                obj.Vertex(ar([-cardDim[0]*backScale,0.3,cardDim[1]*backScale,1])),
                                                obj.Vertex(ar([-cardDim[0]*backScale,0.3,-cardDim[1]*backScale,1])),
                                                obj.Vertex(ar([cardDim[0]*backScale,0.3,-cardDim[1]*backScale,1])),
                                                obj.Vertex(ar([cardDim[0]*backScale,0.3,cardDim[1]*backScale,1])),
                                                ],
                                                virtualCamera=virtualCamera,
                                                planeImage=cardBacksideStr,
                                                planeImageScale=(95,95)))
            
            super().__init__(letterFaceList,
                             position=ar([self.gridPos[0]*gameSettings.cardOffset[0],-9,self.gridPos[1]*gameSettings.cardOffset[1],1]), # make sure this cards world position is consistent with its grid position
                             triangulate=False)


            
    def StartFlip(self) -> None:
        """Start the turn animation of this card."""

        if not self.isTurning:
            self.degreesTurned = 0
            self.isTurning = True

            self.turnedUp = not self.turnedUp # turn around this card
            


    def AnimateFlip(self,turnSpeed: float = gameSettings.flipCardSpeed) -> None:
        """Update the flip animation. Called every frame."""

        # rotate the card
        if self.degreesTurned <= 180:
            ang = turnSpeed*Time.deltaTime
            self.Rotate(ang,0,0)
            self.degreesTurned += ang

        else:

            self.Rotate(180-self.degreesTurned,0,0) # rotate the card slightly back so it doesnt overturn
            self.degreesTurned = 0
            self.isTurning = False

            if self.turnedUp == False:
                self.SetEnabledContentFace(False)

    def Update(self) -> None:
        """Update this memory card. Should be called every frame."""
        if self.isTurning:
            self.AnimateFlip()

    def ObjectClicked(self):
        """Called when this memory card is clicked. 
        Turns around the card if the conditions are right."""

        if len(self.game.selectedCards) < 2 and self.isTurning == False and self.found == False and self not in self.game.selectedCards: # do not let this card be selected if it is already turning

            self.game.selectedCards.append(self) # mark this card as selected


            self.StartFlip()

            self.game.guesses += 1 # increase the guess counter

            # show the content side of this card if it is turned up
            if self.turnedUp == True:
                self.SetEnabledContentFace(True)

    def SetEnabledContentFace(self,enabled):
        """Enables or disables the faces containing the card content of this memory card."""
        for obj in self.faceList:
            if obj.planeImage != cardBacksideStr: # dont enable/disable the backside of the card
                obj.enabled = enabled

            

            


        