import numpy
from numpy import array as ar
from virtualCamera import VirtualCamera 
import Objects3D as O3D
from Vec import Vector3 as V3
from math import cos,sin
from math import pi
import canvas
from typing import List
import copy
import polygon as pg
from Vec import Vector2
import math
import Time


class Renderer():
    def __init__(self,
                 canvas: canvas.Canvas, # the canvas this renderer will render on
                 camera = VirtualCamera(pitch = 0,yaw=0,position=V3(0,0,0))
                ) -> None:
        
        self.canvas = canvas
        self.camera = camera

        self.objectList: List[ar] = []
        """List of 3d objects that this renderer can render."""

        # test tetrahedron (testrahedron :D )
        self.tetrahedron = O3D.CreateTetrahedron(ar([1, 1, 2, 1]), ar([1, 2, 1, 1]), ar([1, 3, 3, 1]), ar([0, 0, 0, 1]), position=ar([0, 0, 0, 1]))
        self.objectList.append(self.tetrahedron)
        self.objectList[0].position += ar([1,0,0,0])

        self.baba = O3D.CreateTetrahedron(ar([1, -1, 1, 1]), ar([-1, -1, 1, 1]), ar([-1, -1, -1, 1]), ar([1, 1, 1, 1]), position=ar([0, 0, 0, 1]))
        self.objectList.append(self.baba)
        self.objectList[1].position += ar([0,5,0,0])


    def GetNearClipCenter(self):
        fp = self.camera.position + self.camera.GetViewDirectionVector() * self.camera.nearClipPlaneDistance
        return fp



    def GetClipVolumeTransformMatrix(self):
        """Gets the 4x4 matrix that will transform 3d space from the furstrum into the clip volume."""
        
        # furstrum point
        #fp = self.GetNearClipCenter()

        cp = self.camera.position;

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
        
        moveFurstrumToZeroArray = ar([[1,0,0,0],
                                      [0,1,0,0],
                                      [0,0,1,-self.camera.nearClipPlaneDistance],
                                      [0,0,0,1]])
        
        nc = self.camera.nearClipPlaneDistance
        fc = self.camera.farClipPlaneDistance
        scaleFactor = 1/(fc-nc) # by which factor the furstrum should be scaled down on the z axis to fit in the clipping volume (z from 0 to 1)
        scalingMatrix =           ar([
                                     [1,0,0,0],
                                     [0,1,0,0],
                                     [0,0,scaleFactor,0],
                                     [0,0,0,1],
                                     ])
        
        # might be some errors here based on order of multiplication maybe
        M = scalingMatrix @ moveFurstrumToZeroArray @ rotateToZAxisArray @ rotateXAxisArray @ rotateYAxisArray @ moveMatrix
        #M = moveMatrix @ rotateXAxisArray @ rotateYAxisArray @ rotateToZAxisArray @ scalingMatrix


        return M
    

    def GetTransformedObjectList(self) -> List[O3D.R3Object]:
        """Get a list of all the objects in this renderer transformed, to render."""

        

        # the matrix all points should be transformed with
        transformMatrix = self.GetClipVolumeTransformMatrix()

        # list of all objects after they have been transformed
        transformedObjectList = copy.deepcopy(self.objectList)
        

        for index,object in enumerate(transformedObjectList):
            for vertex in object.vertexList:

                moveMatrix = ar([[1,0,0,self.objectList[index].position[0]],
                                 [0,1,0,self.objectList[index].position[1]],
                                 [0,0,1,self.objectList[index].position[2]],
                                 [0,0,0,1]])
                


                pos = moveMatrix @ vertex.position

                #position after applying the transform.
                tPos = transformMatrix @ pos

                XsPos = tPos[0]/((self.camera.aspectRatio[0]/2)*(1-tPos[2])+(self.camera.farClipPlaneDistance*self.camera.aspectRatio[0]/(self.camera.nearClipPlaneDistance*2))*(tPos[2]))
                YsPos = tPos[1]/((self.camera.aspectRatio[1]/2)*(1-tPos[2])+(self.camera.farClipPlaneDistance*self.camera.aspectRatio[1]/(self.camera.nearClipPlaneDistance*2))*(tPos[2]))

                # scaled position, scale the view clip volume to have the same dimensions as amount of pixels in the canvas
                sPos = ar([(XsPos+1)*self.canvas.pixelAmountX/2,
                           (YsPos+1)*self.canvas.pixelAmountY/2,
                           tPos[2]])
                
                vertex.position = sPos

        return transformedObjectList
    


    def RenderScene(self):

        for pixelRow in self.canvas.pixelList:
            for pixel in pixelRow:
                pixel.depthBuffer = 1

        self.camera.MoveCamera() # move around the camera

        self.canvas.polygonList = []

        objectList = self.GetTransformedObjectList()

        for object in objectList:
            for polygon in object.faceList:

                newVertexList = []
                oneVertInClipVolume = False
                for vertex in polygon.vertexList:
                    
                    if oneVertInClipVolume == False:
                        if (vertex.position[0] >= 0 and vertex.position[0] <= self.canvas.pixelAmountX) and (vertex.position[1] >= 0 and vertex.position[1] <= self.canvas.pixelAmountY) and (vertex.position[2] >= 0 and vertex.position[2] < 1):
                            oneVertInClipVolume = True

                    newVertexList.append(pg.Vertex(round(vertex.position[0]),round(vertex.position[1])))

                if oneVertInClipVolume == True:

                    planeNormalVector = polygon.GetPlaneEquation()
                    self.canvas.polygonList.append(pg.Polygon(newVertexList,self.canvas,color=polygon.color,equationVector=planeNormalVector))

        self.canvas.RenderAllPolygons()

        

        

                
            




                


        

        


#renderer = Renderer()
#matrix = renderer.GetClipVolumeTransformMatrix()
#print(str(renderer.camera.GetViewDirectionVector()))
#print(matrix)

#print(numpy.linalg.det(matrix))


#nc = renderer.GetNearClipCenter()
#transformed_nc = matrix @ numpy.array([nc.x, nc.y, nc.z, 1])
#transformed_nc = matrix @ numpy.array([2, 0, 0, 1])
#print(transformed_nc)
