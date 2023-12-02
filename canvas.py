"""Module containing the canvas class, used for rendering the game."""

import settings
from Vec import Vector2
import Vec
from typing import List
from pixel import Pixel
from polygon import Polygon

class Canvas():
    """A class used to render the 3d space onto the screen.
    Contains referencecs to every pixel on the screen."""
    def __init__(self,
                 game,
                 pixelAmountX: int = settings.PIXELXAMOUNT,
                 pixelAmountY: int = settings.PIXELYAMOUNT) -> None:
        """Initialize the class and create a pygame rect
        for every pixel on the screen."""

        self.game = game

        self.pixelList: list[Pixel] = []
        """A list of all pixels on the screen."""
        
        self.polygonList: list[Polygon] = []
        """A list of all polygons that should be drawn on this canvas."""

        self.updatedPixelList: list[Pixel] = []
        """list of pixels to re-render this frame, updated pixels."""


        self.pixelAmountX = pixelAmountX
        self.pixelAmountY = pixelAmountY
        # how big of a step, in screen pixels, there will be between each drawn pixel
        self.pixelStepX = settings.WIDTH / pixelAmountX
        self.pixelStepY = settings.HEIGHT / pixelAmountY

        for x in range(self.pixelAmountX):
            pixelRowList = []
            for y in range(self.pixelAmountY):
                pixelRowList.append(Pixel(self,x * self.pixelStepX,y * self.pixelStepY,color=(0,0,0),yCoord=settings.PIXELYAMOUNT-y,xCoord=x)) # multiply the pixels positions with the step value
            self.pixelList.append(pixelRowList)


        

    def Refresh(self,displaySurface) -> Pixel:

        
        for pixel in self.updatedPixelList:
            pixel.Render(displaySurface)

        self.updatedPixelList.clear()


    def getPixel(self,xpos,ypos) -> Pixel:
        if (xpos >= 0 and xpos <= self.pixelAmountX) and (ypos >= 0 and ypos <= self.pixelAmountY):
            try:
                return(self.pixelList[xpos][-ypos]) # negative ypos so that increases in y value results in an increase in "altitude"
            except IndexError:
                return None
        else:
            return None
    
    def getPixelsBetween(self, point1: Vector2, point2: Vector2) -> List[Pixel]:
        """returns a linear list of all pixels between point 1 and point 2"""

        returnList = []

        x1,x2 = int(point1.x),int(point2.x)
        y1,y2 = int(point1.y),int(point2.y)

        rowList = self.pixelList[x1:x2]
        for yList in rowList:
            AppendPixels = yList[-y2:-y1] # negative so that y=0 will be at the bottom of the screen
            for pixel in AppendPixels:
                returnList.append(pixel)

        return returnList
    


    def RenderAllPolygons(self,
                          renderingInformation = None, # class containing information used to render this face
                          ) -> None:
        

        for polygon in self.polygonList:
            polygon.DrawFilled(renderingInformation)




    def DrawCircle(self, position: Vector2, radius: float, color: str = "red"):
        bottomLeftCorner = Vector2(position.x - radius, position.y - radius)
        topRightcorner = Vector2(position.x + radius, position.y + radius)

        pixelList = self.getPixelsBetween(bottomLeftCorner,topRightcorner)
        for pixel in pixelList:

            if Vec.Distance(pixel.coordinates,position) <= radius:

            
                pixel.color = color
                self.updatedPixelList.append(pixel)

    





        








        

    


        

    
            




        

    




                

    

            

            

