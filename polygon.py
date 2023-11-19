from Vec import Vector2
from slopeEquation import SlopeEquation
import settings
import numpy as np
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
                 planeImage = None,
                 camera = None):
        
        self.vertexList = vertexList
        self.canvas = canvas

        self.color = color

        self.equationList = []

        self.equationVector = equationVector

        self.planeImage = planeImage

        self.camera = camera

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
    


    def DrawFilled(self, planeImage: PlaneImage = None) -> None:
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
                                pass
                                





                            touchedPixel.color = self.color
                            self.canvas.updatedPixelList.append(touchedPixel)


    def ReversePerspectiveForPixel(self,x,y, depth, camera) -> List[float]:
        """Return x and y position of a pixel BEFORE its position was transformed for perspective"""

        dimensions = [self.canvas.pixelAmountX,self.canvas.pixelAmountY]

        returnList = []
        for index, var in enumerate([x,y]):
            var *= 2/dimensions[index]
            term1 = var * (camera.aspectRatio[0] / 2) * (1 - depth)
            term2 = var * (camera.farClipPlaneDistance * camera.aspectRatio[0]) / (camera.nearClipPlaneDistance * 2) * depth
            tPos = term1 + term2

            returnList.append(tPos)
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
        




