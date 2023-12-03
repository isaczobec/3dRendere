"""Module that contains classes that can render a 2d polygon on the screen."""

from Vec import Vector2
from slopeEquation import SlopeEquation
import settings
import numpy as np
from image import PlaneImage
from typing import List
from virtualCamera import VirtualCamera
from renderingInformation import RenderingInformation
import mathFunctions as MF

import rgbBlendModes as rgbBlend

class Vertex():
    """A 2d vertex in the screen space (as opposed to in
    the 3d world space)."""
    def __init__(self,
                 xpos: float,ypos: float,
                 worldNormal : np.ndarray = None,
                 ):
        """Init the vertex. Stores its values inside it."""
        
        self.pos = Vector2(xpos,ypos)


        self.worldPosition = None # position in the world. Used to calculate smooth lighting.
        self.worldNormal = worldNormal # normal of this vertex.
        

class Polygon():
    """A 2d polygon in the screen space (as opposed to in
    the 3d world space). Can calculate the correct
    color for every pixrl and be rendered onto the screen."""
    def __init__(self,
                 vertexList: list[Vertex],
                 canvas,
                 color = (255,255,255), 
                 equationVector = np.array([0,0,0]),
                 normalVector = np.array([0,0,0]),
                 planeImage: PlaneImage = None, # the image to be rendered onto this polygon. None if this polygon has no image.
                 planeImageScale: float = 1, # The scale at which the plane image is rendered
                 camera: VirtualCamera = None, # the camera used to render this polygon
                 imageTransformMatrix: np.array = None, # the matrix used to get pixel positions for images on this plane. None if it doesnt have an image
                 drawSmooth: bool = False,
                 ): 
        """Init this polygon. Creates slope equations between
        all its verticies."""
        
        self.vertexList = vertexList
        self.canvas = canvas

        self.color = color

        self.equationList = []

        self.equationVector = equationVector
        self.normalVector = normalVector

        self.planeImage = planeImage
        self.planeImageScale = planeImageScale
        self.camera = camera
        self.imageTransformMatrix = imageTransformMatrix

        self.drawSmooth = drawSmooth

        self.CreateSlopeEquationsBetweenVerticies()

        self.bounds = self.GetBounds()

    def CreateSlopeEquationsBetweenVerticies(self) -> None:
        """Creates slope equations between all this
        polygons vertecies and stores them in this polygon's equationlist."""

        for index,vertex in enumerate(self.vertexList):
            nextVertex = self.vertexList[(index + 1) % len(self.vertexList)] # get the next vertex adjacent to this one

            if vertex.pos.x > nextVertex.pos.x:
                equation = SlopeEquation(minXLimit=nextVertex.pos.x,maxXLimit=vertex.pos.x)
            else:
                equation = SlopeEquation(minXLimit=vertex.pos.x,maxXLimit=nextVertex.pos.x)
            equation.AdjustToTwoPoints(vertex.pos,nextVertex.pos)

            self.equationList.append(equation)

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



    def DrawFilled(self, 
                   renderingInformation: RenderingInformation = None, # a class containing rendering information used to draw the polygons
                   ) -> None:
        """Calculates the color of all the pixels of this polygon.
        calculates correct lighting and pixel color of potential images
        to be rendered on this polygon."""

        # get the bounds of this polygon; the area of pixels to do calculations for
        minY = self.bounds[0].y
        minX = self.bounds[0].x
        maxY = self.bounds[1].y
        maxX = self.bounds[1].x

        # store world position of vertexes. Necesary for rendering smooth surfaces.
        if self.drawSmooth:
            for vertex in self.vertexList:
                vertex.worldPosition = self.GetPixelPolygonPosition(vertex.pos.x,vertex.pos.y,self.GetDepth(vertex.pos.x,vertex.pos.y))

        
        if self.drawSmooth == False:
            sunLightFactor = self.GetSunlightFactor(renderingInformation,self.normalVector)
        #print(f"normalvector: {self.normalVector} sunLightVector: {renderingInformation.sunLightDirection} factor: {sunLightFactor}")

        #normalFactor = np.clip(np.dot(self.normalVector,renderingInformation.cameraDirectionVector),0,1)
        
        # a horizontal line that is gradually moved up and checks for intersections with polygons
        drawSlope = SlopeEquation(0,0)

        # iterate through every row of pixels in this polygon
        for yOffset in range(maxY-minY):
            y = minY + yOffset

            intersectXList = self.GetHorizontalIntersectionList(drawSlope, y)

            if len(intersectXList) <= 1: # if there were no or just one interection on this y-coordinate, move up
                continue

            draw = False 

            intersectXSet = set(intersectXList) # convert the list to a set for faster list searching
            # iterate through every pixel in this row of pixels
            for xOffset in range(maxX-minX):
                x = xOffset + minX
                if x in intersectXSet:
                    draw = not draw # toggle drawing pixels if an edge of the polygon is hit

                # Calculating the color of a pixel:
                if draw:
                    self.CalculatePixelColor(renderingInformation, sunLightFactor, y, x)


    def CalculatePixelColor(self, 
                            renderingInformation: RenderingInformation, 
                            sunLightFactor : float, 
                            y: int, 
                            x: int,
                            ) -> None:
        """Calculates the color of the pixel at coordinates (x,y)."""

        touchedPixel = self.canvas.GetPixel(x,y)
        if touchedPixel != None:

            depth = self.GetDepth(x,y)
            #only render the pixel if it is in front of the last rendered pixel
            if touchedPixel.depthBuffer > depth:
                touchedPixel.depthBuffer = depth

                if self.planeImage != None:
                    # get the color of the planeImage at this pixel
                    pixelPosition = self.GetPixelPolygonPosition(x,y,depth)
                    imageColor = self.planeImage.SampleRGB(pixelPosition[0],pixelPosition[1],scale=self.planeImageScale)
                    touchedPixel.color = imageColor

                else:
                    touchedPixel.color = self.color

                # apply sunlight
                if self.drawSmooth == True: # Smooth shading was not used in the final game
                    finalSunColor = rgbBlend.ScalarMultiply(renderingInformation.sunColor,self.GetSunlightFactor(renderingInformation,self.InterpolateVertexNormals(x,y)))
                else:
                    finalSunColor = rgbBlend.ScalarMultiply(renderingInformation.sunColor,sunLightFactor)

                touchedPixel.color = rgbBlend.Multiply(touchedPixel.color,finalSunColor)

                # append the pixel to a list of pixels to re-render this frame
                self.canvas.updatedPixelList.append(touchedPixel)



    def GetHorizontalIntersectionList(self, drawSlope: SlopeEquation, y: int) -> list[Vector2]:
        """gets and returns a list of all intersections 
        between an ofset horizontal line and this polygon."""

        drawSlope.offset = y
        intersectXList = []
        for equation in self.equationList:
            intersectPoint = drawSlope.GetIntersection(equation)
            if intersectPoint != None:
                intersectPointRoundedX = round(intersectPoint.x)
                if intersectPointRoundedX not in intersectXList:
                    intersectXList.append(intersectPointRoundedX)
        intersectXList.sort()
        return intersectXList

    def GetSunlightFactor(self,renderingInformation,normal) -> float:
        """Gets the factor (between 0 and 1) of the sunlight on the normal."""
        sunLightFactor = np.clip(np.dot(normal,renderingInformation.sunLightDirection),renderingInformation.sunCap,1)
        return sunLightFactor

    def InterpolateVertexNormals(self,x,y) -> np.ndarray:
        """Calculates the normal at an x,y value of this polygon using bilinear interpolation."""
        # !!! Not used in the final game

        pixelWorldPosition = self.GetPixelPolygonPosition(x,y,self.GetDepth(x,y))

        pixelNormal = np.array([0,0,0])

        for i,vertex in enumerate(self.vertexList):
            area = np.linalg.norm(MF.PerpetualVectorOnVector(pixelWorldPosition - vertex.worldPosition,self.vertexList[(i+1)%len(self.vertexList)].worldPosition)) * np.linalg.norm(self.vertexList[(i+1)%len(self.vertexList)].worldPosition-vertex.worldPosition)/2
            pixelNormal = pixelNormal + self.vertexList[(i+2)%(len(self.vertexList))].worldNormal * area # add the wheighted normal to the pixels normal

        pixelNormal = pixelNormal / np.linalg.norm(pixelNormal)
        return pixelNormal


    def GetPixelPolygonPosition(self,x,y,depth) -> np.ndarray:
        """Gets the position of a pixel on its untransformed vertex. 
        Used for rendering images and calculating smooth shading."""
        rP = self.ReversePerspectiveForPixel(x,y,depth,self.camera) # reverse the perspective of this pixel and get the original x,y position of it

        #if self.drawSmooth: print("transformMatrix:",self.imageTransformMatrix,"posvector",np.array([rP[0],rP[1],depth,1]))
        pixelPosition = self.imageTransformMatrix @ np.array([rP[0],rP[1],depth,1]) # transform this pixels position to get the x,y of the image it is supposed to display

        return pixelPosition

    

    def ReversePerspectiveForPixel(self,x,y, depth, camera) -> List[float]:
        """Return x and y position of a pixel BEFORE 
        its position was transformed for perspective"""

        dimensions = [self.canvas.pixelAmountX,self.canvas.pixelAmountY]

        returnList = []
        for index, var in enumerate([x,y]):

            # reverse the scaling to fit the screen of the position
            var *= (2/dimensions[index])
            var -= 1

            # the reverse operation of the mathematical function that moves verticies for perspective
            var = var * ((camera.aspectRatio[index]/2)*(1-depth)+(camera.farClipPlaneDistance*camera.aspectRatio[index]/(camera.nearClipPlaneDistance*2))*(depth))

            returnList.append(var)
        return returnList 



    def GetDepth(self,x:float,y:float) -> float:
        """returns the depth of a point on this polygon"""

        depth = (self.equationVector[3] - self.equationVector[0] * x - self.equationVector[1] * y) / self.equationVector[2]
        return depth

    def CheckIfPointInPolygon(self,x: float,y: float) -> bool:
        """Checks if x,y lies in the polygon. Returns a bool."""

        # create a vertical line at the x position
        verticalLine = SlopeEquation()
        verticalLine.vertical = True
        verticalLine.xVerticalPosition = x/2 # divided by two since there was a problem with scaling otherwise

        # create a horizontal line at the y position
        horizontalLine = SlopeEquation(0, y/2)

        HIntersections = []
        VIntersections = []
        for equation in self.equationList:

            self.CheckAndAppendIntersection(horizontalLine, HIntersections, equation)
            self.CheckAndAppendIntersection(verticalLine, VIntersections, equation)

        # return true if both the vertical and horizontal lines hit something
        if len(HIntersections) == 0 or len(VIntersections) == 0:
            return False
        else:
            return True
        
        # this doesnt really check if a position is strictly withing a polygon, rather if it is inside its bounding box.
        # but it works well enough for the memory game.

    def CheckAndAppendIntersection(self, 
                                   Line: SlopeEquation,
                                   Intersections: list[Vector2], 
                                   equation: SlopeEquation
                                   ) -> None:
        """Checks if two equations intersect and
        appends the intersection to a list if they do."""
        intersection = Line.GetIntersection(equation)
        if intersection != None:
            if intersection.x >= equation.minXLimit and intersection.x <= equation.maxXLimit:
                Intersections.append(intersection)
        






            


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
                    self.canvas.GetPixel(round(penPos.x),round(penPos.y)).color = (255,255,255)
                    penPos.x += movementVec.x
                    penPos.y += movementVec.y
            else:
                while penPos.x > nextVertex.pos.x:
                    self.canvas.GetPixel(round(penPos.x),round(penPos.y)).color = (255,255,255)
                    penPos.x += movementVec.x
                    penPos.y += movementVec.y



    def DrawOutlinesWithEquations(self):
        for equation in self.equationList:
            equation.DrawSlopeLine(self.canvas)

