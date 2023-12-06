"""A module with the renderer class."""

from numpy import array as ar
import numpy as np
from virtualCamera import VirtualCamera 
import Objects3D as O3D
from Vec import Vector3 as V3
from math import cos,sin,pi,isnan,isinf
import canvas
from typing import List
import copy
import polygon as pg
import math
import inputHandler
from renderingInformation import RenderingInformation
import image
import Time




class Renderer():
    """The 3d renderer. Responsible for transforming 3D
    space into a view volume and rendering all 3d objects.
    Contains references to all 3d objects that should be rendered."""
    def __init__(self,
                 canvas: canvas.Canvas, # the canvas this renderer will render on
                 camera = VirtualCamera(pitch = 0,yaw=0,position=V3(0,0,0)),
                 lightDirection = ar([0,-1,0]) 
                ) -> None:
        """Init the renderer. Create the object list, camera and canvas.
        also creates an imageHandler."""
        
        self.canvas = canvas
        self.camera = camera

        self.rendenderingInformation = RenderingInformation(lightDirection,(255,255,255),0.33,self.camera.GetViewDirectionVector())

        

        self.mouseInputHandler = inputHandler.MouseInputHandler()

        self.objectList: List[ar] = []
        """List of 3d objects that this renderer can render."""

        # test tetrahedron (testrahedron :D )
        # self.tetrahedron = O3D.CreateTetrahedron(ar([1, 1, 2, 1]), ar([1, 2, 1, 1]), ar([1, 3, 3, 1]), ar([0, 0, 0, 1]), position=ar([0, 5, 0, 1]),renderSmooth=True)
        
        # self.objectList.append(self.tetrahedron)

        #self.baba = O3D.CreateTetrahedron(ar([2, 1, -1, 1]), ar([-1, -1, 1, 1]), ar([-1, -1, -1, 1]), ar([1, 1, 1, 1]), position=ar([0, 0, 0, 1]))
        #self.objectList.append(self.baba)
        #elf.objectList[1].position += ar([0,0,0,0])

        
        # self.sphere = O3D.CreateUVSphere(1,20,10,ar([3,0,0,1]),color=(0,255,0),triangulateFaces=False)
        # self.objectList.append(self.sphere)

        

        self.clickedObject = None
        """The 3d object that was clicjed this frame."""


        # Create an image reference list. 
        self.imageHandler = image.ImageHandler({
            "cardBackside":"images/cardBackside.jpeg",
            "cat":"images/cat.jpg",
            "dora":"images/goofy.jpg",
            "a":"images/letters/a (1).png",
            "b":"images/letters/b (1).png",
            "c":"images/letters/c (1).png",
            "d":"images/letters/d (1).png",
            "e":"images/letters/e (1).png",
            "f":"images/letters/f (1).png",
            "g":"images/letters/g (1).png",
            "h":"images/letters/h (1).png",
            "i":"images/letters/i (1).png",
            "j":"images/letters/j (1).png",
            "k":"images/letters/k (1).png",
            "l":"images/letters/l (1).png",
            "m":"images/letters/m (1).png",
            "n":"images/letters/n (1).png",
            "o":"images/letters/o (1).png",
            "p":"images/letters/p (1).png",
            "q":"images/letters/q (1).png",
            "r":"images/letters/r (1).png",
            "s":"images/letters/s (1).png",
            "t":"images/letters/t (1).png",
            "u":"images/letters/u (1).png",
            "v":"images/letters/v (1).png",
            "w":"images/letters/w (1).png",
            "x":"images/letters/x (1).png",
            "y":"images/letters/y (1).png",
            "z":"images/letters/z (1).png",
            "å":"images/letters/å (1).png",
            "ä":"images/letters/ä (1).png",
            "ö":"images/letters/ö (1).png",
        })


    def GetNearClipCenter(self) -> np.ndarray:
        """Returns the world space position
        of the center of the camera's near clip plane."""
        fp = self.camera.position + self.camera.GetViewDirectionVector() * self.camera.nearClipPlaneDistance
        return fp



    def GetClipVolumeTransformMatrix(self) -> np.ndarray:
        """Gets the 4x4 matrix that will transform 3d space 
        from the furstrum into the clip volume."""
        
        # furstrum point
        #fp = self.GetNearClipCenter()

        cp = self.camera.position

        # move the furstrums center to 0,0,0
        moveMatrix =         ar([[1,0,0,-cp.x],
                                 [0,1,0,-cp.y],
                                 [0,0,1,-cp.z],
                                 [0,0,0,1]])
        
        # rotate transform based on the cameras rotation, rotate it back to normal
        yaw = self.camera.yaw
        pitch = self.camera.pitch
        rotateYAxisArray =          ar([[cos(-yaw),0,sin(-yaw),0],
                                        [0,1,0,0],
                                        [-sin(-yaw),0,cos(-yaw),0],
                                        [0,0,0,1]])
        
        rotateXAxisArray =          ar([
                                        [cos(-pitch),sin(-pitch),0,0],
                                        [-sin(-pitch),cos(-pitch),0,0],
                                        [0,0,1,0],
                                        [0,0,0,1]
                                        ])
        
        #Array that rotates a vector 90 degrees on the y-axis, so that z will be depth of the furstrum
        rotateToZAxisArray =          ar([[0,0,-1,0],
                                          [0,1,0,0],
                                          [1,0,0,0],
                                          [0,0,0,1],
                                          ])
        
        # moves the center of the near clip plane to 0,0,0
        moveFurstrumToZeroArray = ar([[1,0,0,0],
                                      [0,1,0,0],
                                      [0,0,1,-self.camera.nearClipPlaneDistance],
                                      [0,0,0,1]])
        
        scaleFactor = self.camera.GetScalingFactor() # by which factor the furstrum should be scaled down on the z axis to fit in the clipping volume (z from 0 to 1)
        scalingMatrix =           ar([
                                     [1,0,0,0],
                                     [0,1,0,0],
                                     [0,0,scaleFactor,0],
                                     [0,0,0,1],
                                     ])
        
        # apply all matricies one after the other
        M = scalingMatrix @ moveFurstrumToZeroArray @ rotateToZAxisArray @ rotateXAxisArray @ rotateYAxisArray @ moveMatrix

        return M
    
    

    def GetTransformedObjectList(self) -> List[O3D.R3Object]:
        """Applies the view transforms to all objects 
        and returns a list of them."""

        # the matrix all points should be transformed with
        transformMatrix = self.GetClipVolumeTransformMatrix()

        # list of all objects after they have been transformed
        # copy it since the world position of all objects should stay the same
        transformedObjectList: List[O3D.R3Object] = copy.deepcopy(self.objectList)

        for index,object in enumerate(transformedObjectList):

            if object != None: # only do the transformations if the object is enabled

                for vertex in object.vertexList:

                    # move the objects according to their world position offset
                    moveMatrix = ar([[1,0,0,self.objectList[index].position[0]],
                                    [0,1,0,self.objectList[index].position[1]],
                                    [0,0,1,self.objectList[index].position[2]],
                                    [0,0,0,1]])
                    
                    pos = moveMatrix @ vertex.position


                    # Apply the view volume transform.
                    tPos = transformMatrix @ pos

                    vertex.position = tPos

                for face in object.faceList:
                    if face != None: # disabled faces are copied as None; do not do anything with them
                        if face.planeImage != None:
                            face.imageTransformMatrix = face.GetImageTransformMatrix() # save the image transform matrix for this face

                    # !!! smooth rendering was not used in the final game !!!
                    if self.objectList[index].renderSmooth == True:

                        face.virtualCamera = self.camera
                        face.imageTransformMatrix = face.GetImageTransformMatrix()


                for vertex in object.vertexList:

                    tPos = vertex.position

                    # use a formula to move every point to account for perspective
                    # Every point that is withing the clip volume has a x,y value within -1 to 1
                    XsPos = tPos[0]/((self.camera.aspectRatio[0]/2)*(1-tPos[2])+(self.camera.farClipPlaneDistance*self.camera.aspectRatio[0]/(self.camera.nearClipPlaneDistance*2))*(tPos[2]))
                    YsPos = tPos[1]/((self.camera.aspectRatio[1]/2)*(1-tPos[2])+(self.camera.farClipPlaneDistance*self.camera.aspectRatio[1]/(self.camera.nearClipPlaneDistance*2))*(tPos[2]))

                    # prevent a value error
                    if math.isnan(XsPos) or math.isinf(XsPos):
                        XsPos = 0
                    if math.isnan(YsPos) or math.isinf(YsPos):
                        YsPos = 0

                    # scaled position, scale the view clip volume to have the same dimensions as amount of pixels in the canvas (makes rendering pixels easier)
                    sPos = ar([
                                (XsPos+1)*self.canvas.pixelAmountX/2,
                                (YsPos+1)*self.canvas.pixelAmountY/2,
                                tPos[2],
                                1
                            ]
                            )
                    
                    vertex.position = sPos

        return transformedObjectList
    


    def RenderScene(self) -> None:
        """Renders objects in this scene. Should be ran every frame."""

        # reset the depth buffer of all pixels
        for pixelRow in self.canvas.pixelList:
            for pixel in pixelRow:
                pixel.depthBuffer = 1

        self.camera.MoveCamera() # move around the camera

        self.canvas.polygonList = []

        objectList = self.GetTransformedObjectList()


            
        mouseInput = self.mouseInputHandler.GetMouseInput() # None if the player didnt click this frame

        clickedObject: O3D.R3Object = None
        """The object that was clicked this frame. None if no object was clicked."""

        clickedObjectDepthBuffer = 1
        """The depth of the clicked object. Used to get the first object in the line of sight clicked."""

        # iterate through all transformed objects
        for objectIndex, object in enumerate(objectList):
            if object != None: # only render the object if it is enabled; is not None
            
                for polygonIndex, polygon in enumerate(object.faceList):
                    if polygon != None: # only render the polygon if it is enabled; is not None

                        newVertexList = []
                        oneVertInClipVolume = False
                        for vertex in polygon.vertexList:
                            
                            #Check if the polygon is inside the clip volume, and only render it if it is
                            if oneVertInClipVolume == False:
                                if (vertex.position[0] >= 0 and vertex.position[0] <= self.canvas.pixelAmountX) and (vertex.position[1] >= 0 and vertex.position[1] <= self.canvas.pixelAmountY) and (vertex.position[2] >= 0 and vertex.position[2] < 1):
                                    oneVertInClipVolume = True

                            # create 2d screen space verticies from the 3d world space verticies
                            # !! smooth rendering was ultimately not used in the final game !!!
                            if self.objectList[objectIndex].hasVertexNormals and self.objectList[objectIndex].renderSmooth:
                                newVertexList.append(pg.Vertex(round(vertex.position[0]),round(vertex.position[1]),worldNormal=vertex.normal))
                            else:
                                newVertexList.append(pg.Vertex(round(vertex.position[0]),round(vertex.position[1])))


                        if oneVertInClipVolume == True:

                            planeEquation = polygon.GetPlaneEquation()
                            unTransformedNormalVector = self.objectList[objectIndex].faceList[polygonIndex].GetNormalVector() # get the plane normal vector of from the original, untransformed face

                                #for vertex in polygon.vertexList:
                                #    print("vertPos:",vertex.position)

                            
                            # create a 2d screen space polygon for rendering and pass in all arguments
                            canvasPolygon = pg.Polygon(newVertexList,self.canvas,color=polygon.color,equationVector=planeEquation,normalVector=unTransformedNormalVector,planeImage=self.imageHandler.GetImage(polygon.planeImage),planeImageScale=polygon.planeImageScale,camera=self.camera,imageTransformMatrix=polygon.imageTransformMatrix,drawSmooth=self.objectList[objectIndex].renderSmooth)

                            self.canvas.polygonList.append(canvasPolygon)

                            # Check if this polygon was clicked
                            if mouseInput != None:

                                if canvasPolygon.CheckIfPointInPolygon(mouseInput[0],mouseInput[1]):

                                    # only set this object to the clicked one if it isnt behind any other object
                                    polyonDepth = canvasPolygon.GetDepth(mouseInput[0],mouseInput[1])
                                    if polyonDepth < clickedObjectDepthBuffer:
                                        clickedObjectDepthBuffer = polyonDepth

                                        clickedObject = self.objectList[objectIndex]

                            
        self.clickedObject = clickedObject
        #if clickedObject != None:

            #print(clickedObject)
            #for face in clickedObject.faceList:
            #   face.color = (255,0,0)

        # pass the cameras direction vector to ther renderinginformation object
        cameraVectorOtherType = self.camera.GetViewDirectionVector()
        cameraVector = ar([cameraVectorOtherType.x,cameraVectorOtherType.y,cameraVectorOtherType.z])
        self.rendenderingInformation.cameraDirectionVector = cameraVector # update the direction vector of the camera

        # render all 2d screen space polygons
        self.canvas.RenderAllPolygons(self.rendenderingInformation)



        

        

                
            




                


        

        


#renderer = Renderer()
#matrix = renderer.GetClipVolumeTransformMatrix()
#print(str(renderer.camera.GetViewDirectionVector()))
#print(matrix)

#print(numpy.linalg.det(matrix))


#nc = renderer.GetNearClipCenter()
#transformed_nc = matrix @ numpy.array([nc.x, nc.y, nc.z, 1])
#transformed_nc = matrix @ numpy.array([2, 0, 0, 1])
#print(transformed_nc)
