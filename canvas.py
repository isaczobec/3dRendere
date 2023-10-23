import pygame
import settings
from Vec2 import Vector2
import Vec2
import random
from typing import List







class Canvas():
    def __init__(self,game,pixelAmountX: int = settings.PIXELXAMOUNT,pixelAmountY: int = settings.PIXELYAMOUNT) -> None:
        self.game  = game

        self.pixelList = []
        self.polygonList = []

        self.updatedPixelList = [] # list of pixels to re-render this frame, updated pixels


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

    def Refresh(self,displaySurface):
        
        for pixel in self.updatedPixelList:
            pixel.Render(displaySurface)

        self.updatedPixelList.clear()

    def getPixel(self,xpos,ypos):
        return(self.pixelList[xpos][-ypos]) # negative ypos so that increases in y value results in an increase in "altitude"
    
    def getPixelsBetween(self, point1: Vector2, point2: Vector2) -> List:
        """returns a linear list of all pixels between point 1 and point 2"""

        returnList = []

        rowList = self.pixelList[point1.x:point2.x]
        for yList in rowList:
            AppendPixels = yList[-point2.y:-point1.y] # negative so that y=0 will be at the bottom of the screen
            for pixel in AppendPixels:
                returnList.append(pixel)

        return returnList




    def DrawCircle(self, position: Vector2, radius: float, color: str = "red"):
        bottomLeftCorner = Vector2(position.x - radius, position.y - radius)
        topRightcorner = Vector2(position.x + radius, position.y + radius)

        pixelList = self.getPixelsBetween(bottomLeftCorner,topRightcorner)
        for pixel in pixelList:

            if Vec2.Distance(pixel.coordinates,position) <= radius:

            
                pixel.color = (255,0,0)
                self.updatedPixelList.append(pixel)

        

class Pixel():
    def __init__(self,canvas: Canvas,xpos,ypos,xCoord: int, yCoord: int,color=(0,0,0)):

        self.canvas = canvas

        pixelSizeX = settings.WIDTH / canvas.pixelAmountX
        pixelSizeY = settings.HEIGHT / canvas.pixelAmountY


    

        self.pos = Vector2(xpos,ypos)
        self.rect = pygame.rect.Rect(self.pos.x,self.pos.y,pixelSizeX,pixelSizeY)
        self.color = color

        self.coordinates = Vector2(xCoord,yCoord)

    def Render(self,displaySurface):
        pygame.draw.rect(displaySurface,self.color,self.rect)



class Vertex():
    def __init__(self,xpos,ypos):
        self.pos = Vector2(xpos,ypos)
        

class Polygon():
    def __init__(self,vertexList,canvas):
        self.vertexList = vertexList
        self.canvas = canvas

        self.equationList = []

        for index,vertex in enumerate(self.vertexList):

            nextVertex = self.vertexList[(index + 1) % len(self.vertexList)]

            if vertex.pos.x > nextVertex.pos.x:
                equation = SlopeEquation(minXLimit=nextVertex.pos.x,maxXLimit=vertex.pos.x)
            else:
                equation = SlopeEquation(minXLimit=vertex.pos.x,maxXLimit=nextVertex.pos.x)
            equation.AdjustToTwoPoints(vertex.pos,nextVertex.pos)

            self.equationList.append(equation)

        self.bounds = self.GetBounds()



        

    def GetBounds(self) -> Vector2:
        """Returns a list of the bounds of the polygon, [Vector2(minX,minY),Vector2(maxX,maxY)]"""

        # create the bounds of the polygon
        minY = settings.PIXELYAMOUNT
        maxY = 0
        minX = settings.PIXELXAMOUNT
        maxX = 0
        for vertex in self.vertexList: 
            if vertex.pos.y < minY:
                minY = vertex.pos.y
            if vertex.pos.y > maxY:
                maxY = vertex.pos.y
            if vertex.pos.x < minX:
                minX = vertex.pos.x
            if vertex.pos.x > maxX:
                maxX = vertex.pos.x
        return [Vector2(minX,minY),Vector2(maxX,maxY)]


            


    def DrawOutlines(self):
        for index,vertex in enumerate(self.vertexList):

            nextVertex = self.vertexList[(index + 1) % len(self.vertexList)]



            deltaX = nextVertex.pos.x - vertex.pos.x
            deltaY = nextVertex.pos.y - vertex.pos.y

            movementVec = Vector2(deltaX,deltaY)
            movementVec.Normalize()

            penPos = Vector2(vertex.pos.x,vertex.pos.y)
            
            if nextVertex.pos.x > vertex.pos.x:
                while penPos.x < nextVertex.pos.x:
                    self.canvas.getPixel(round(penPos.x),round(penPos.y)).color = (255,255,255)
                    penPos.x += movementVec.x
                    penPos.y += movementVec.y
            else:
                while penPos.x > nextVertex.pos.x:
                    self.canvas.getPixel(round(penPos.x),round(penPos.y)).color = (255,255,255)
                    penPos.x += movementVec.x
                    penPos.y += movementVec.y



    def DrawOutlinesWithEquations(self):
        for equation in self.equationList:
            equation.DrawSlopeLine(self.canvas)
    


    def DrawFilled(self):
        minY = self.bounds[0].y
        minX = self.bounds[0].x
        maxY = self.bounds[1].y
        maxX = self.bounds[1].x

        for yOffset in range(maxY-minY):
            y = minY + yOffset

            drawSlope = SlopeEquation(0,y)
            intersectXList = []
            for equation in self.equationList:
                intersectPoint = drawSlope.GetIntersection(equation)
                if intersectPoint != None:
                    intersectPointRoundedX = round(intersectPoint.x)
                    if intersectPointRoundedX not in intersectXList:
                        intersectXList.append(intersectPointRoundedX)
            intersectXList.sort()



            if len(intersectXList) <= 1:
                continue

            draw = False

            for xOffset in range(maxX-minX):
                x = xOffset + minX
                if x in intersectXList:
                    draw = not draw

                if draw:
                    touchedPixel = self.canvas.getPixel(x,y)
                    touchedPixel.color = (255,255,255)
                    self.canvas.updatedPixelList.append(touchedPixel)


        

    
            


class SlopeEquation():
    def __init__(self,slope = 0,offset = 0,minXLimit = 0,maxXLimit = settings.WIDTH):
        self.slope = slope
        self.offset = offset

        self.minXLimit = minXLimit
        self.maxXLimit = maxXLimit

    def GetY(self,x):
        y = self.slope * x + self.offset
        return y
    
    def AdjustToTwoPoints(self,p1,p2):

        deltaX = p1.x - p2.x
        deltaY = p1.y - p2.y

        self.slope = deltaY/deltaX

        self.offset = p1.y - self.slope * p1.x


    def DrawSlopeLine(self,canvas,color = (255,255,255)):

        for n in range(self.maxXLimit - self.minXLimit):

            x = self.minXLimit + n
            
            y = self.GetY(x)

            if y <= settings.HEIGHT and y >= 0 and x <= settings.WIDTH and x >= 0:
                canvas.getPixel(x,round(y)).color = color

        


    def GetIntersection(self,otherSlopeEquation):

        x = (otherSlopeEquation.offset - self.offset)/(self.slope - otherSlopeEquation.slope)
        y = self.GetY(x)

        if x >= self.minXLimit and x <= self.maxXLimit and x >= otherSlopeEquation.minXLimit and x <= otherSlopeEquation.maxXLimit:

            return Vector2(x,y)
        
        else:
            return None


        #y = kx + m
        # k1x + m1 = k2x + m2
        # m2 - m1 = k1x - k2x
        # m2 - m1 = (k1-k2)x
        # (m2 - m1)/(k1-k2) = x

        

    




                

    

            

            

