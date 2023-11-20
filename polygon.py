from Vec import Vector2
from slopeEquation import SlopeEquation
import settings
import numpy as np
import image
from image import PlaneImage
from typing import List



class Vertex():
    def __init__(self,xpos,ypos):
        self.pos = Vector2(xpos,ypos)
        

class Polygon():
    def __init__(self,
                 vertexList,
                 canvas,
                 color = (255,255,255), 
                 equationVector = np.array([0,0,0]),
                 planeImage = None, # the image to be rendered onto this polygon. None if this polygon has no image.
                 camera = None, # the camera used to render this polygon
                 imageTransformMatrix: np.array = None): # the matrix used to get pixel positions for images on this plane. None if it doesnt have an image
        
        self.vertexList = vertexList
        self.canvas = canvas

        self.color = color

        self.equationList = []

        self.equationVector = equationVector

        self.planeImage = planeImage

        self.camera = camera

        self.imageTransformMatrix = imageTransformMatrix

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


    def GetImageColorAtCoordinate(self,planeImage : PlaneImage,x,y):
        pass
    


    def DrawFilled(self) -> None:
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
                    if touchedPixel != None:

                        depth = self.GetDepth(x,y)

                        #only render the pixel if it is in front of the last rendered pixel
                        if touchedPixel.depthBuffer > depth:

                            touchedPixel.depthBuffer = depth


                            if self.planeImage != None:
                                
                                # get the color of the planeImage at this pixel

                                rP = self.ReversePerspectiveForPixel(x,y,depth,self.camera) # reverse the perspective of this pixel and get the original x,y position of it

                                pixelPosition = self.imageTransformMatrix @ np.array([rP[0],rP[1],depth,1]) # transform this pixels position to get the x,y of the image it is supposed to display
                                imageColor = image.testGetPixelColor(pixelPosition[0],pixelPosition[1],300)
                                touchedPixel.color = imageColor

                            else:
                                touchedPixel.color = self.color
                                
                            self.canvas.updatedPixelList.append(touchedPixel)


    # Got the inverse functions for the perspective equations from chatgpt cause those would be annoying to figure out myself
    def ReversePerspectiveForPixel(self,x,y, depth, camera) -> List[float]:
        """Return x and y position of a pixel BEFORE its position was transformed for perspective"""


        dimensions = [self.canvas.pixelAmountX,self.canvas.pixelAmountY]

        returnList = []
        for index, var in enumerate([x,y]):

            # reverse the scaling to fit the screen of the position
            var *= (2/dimensions[index])
            var -= 1

            var = var * ((camera.aspectRatio[index]/2)*(1-depth)+(camera.farClipPlaneDistance*camera.aspectRatio[index]/(camera.nearClipPlaneDistance*2))*(depth))



            returnList.append(var)
        return returnList 



    def GetDepth(self,x,y) -> float:
        """returns the depth of a point on this polygon"""

        depth = (self.equationVector[3] - self.equationVector[0] * x - self.equationVector[1] * y) / self.equationVector[2]
        return depth

    def CheckIfPointInPolygon(self,x: float,y: float) -> bool:
        """Checks if x,y lies in the polygon. Returns a bool"""


        verticalLine = SlopeEquation()
        verticalLine.vertical = True
        verticalLine.xVerticalPosition = x/2

        horizontalLine = SlopeEquation(0, y/2)

        HIntersections = []
        VIntersections = []
        for equation in self.equationList:

            Hint = horizontalLine.GetIntersection(equation)
            if Hint != None:
                if Hint.x >= equation.minXLimit and Hint.x <= equation.maxXLimit:
                    HIntersections.append(Hint)


            Vint = verticalLine.GetIntersection(equation)
            if Vint != None:
                if Vint.x >= equation.minXLimit and Vint.x <= equation.maxXLimit:
                    VIntersections.append(Vint)

            


        if len(HIntersections) == 0 or len(VIntersections) == 0:
            return False
        else:
            return True
        # Obviously not done yet, just want to see if this works
        




