from Vec import Vector3 as V3
import numpy
from typing import List

class Vertex():
    def __init__(self,
            position: numpy.array = numpy.array([0,0,0])) -> None:
        
        self.position = position
        

class Face():
    def __init__(self,vertexList: List[numpy.array],color: (float,float,float) = (255,255,255), triangulate: bool = True) -> None:

        self.vertexList = vertexList;
        self.color = color

    def Triangulate(self):
        """Divides this face into triangles, returns a list of triangle faces."""

        triangleFaceList = []

        for i in range(len(self.vertexList)):
            triangleFaceList.append()


    def GetPlaneEquation(self) -> numpy.array:
        """returns a 4 dimensional vector, where the first 3 numbers is the normal vector of the plane. The 4th is the right hand side of the equation."""

        basePoint = self.vertexList[0].position
        
        point1Vector: numpy.array = self.vertexList[1].position - self.vertexList[0].position
        point2Vector: numpy.array = self.vertexList[-1].position - self.vertexList[0].position

        planeNormalVector = numpy.cross(point1Vector,point2Vector)

        # calculate what the right side of the planes equation should be, based on the fact that the base point should be on the plane
        equationResult = planeNormalVector[0] * basePoint[0] + planeNormalVector[1] * basePoint[1] + planeNormalVector[2] * basePoint[2]

        equationVector = numpy.array([planeNormalVector[0],planeNormalVector[1],planeNormalVector[2],equationResult])
        

        return equationVector
    
    def GetNormalVector(self):
        point1Vector: numpy.array = self.vertexList[1].position - self.vertexList[0].position
        point2Vector: numpy.array = self.vertexList[-1].position - self.vertexList[0].position


        planeNormalVector = numpy.cross(point1Vector,point2Vector)

        planeNormalVector = planeNormalVector / numpy.linalg.norm(planeNormalVector) # normalize the vector
        return planeNormalVector


        

class R3Object():
    """three-dimensional object consisting of a bunch of vertexes. Created by inputting a list of Faces."""
    def __init__(self, faceList: List[Face], position: numpy.array) -> None:

        self.faceList = faceList

        self.vertexList = self.CreateVertexList()

        self.position = position
        

    def CreateVertexList(self):
        vertexList = []
        for face in self.faceList:
            for vertex in face.vertexList:
                if vertex not in vertexList:
                    vertexList.append(vertex)
        return vertexList
    
    def Move(self,
             x,y,z):
        
        moveMatrix =numpy.array([[1,0,0,x],
                                 [0,1,0,y],
                                 [0,0,1,z],
                                 [0,0,0,1]])
        self.position = moveMatrix @ self.position
        


        
        

def CreateTetrahedron(p1: numpy.array,
                   p2: numpy.array,
                   p3: numpy.array,
                   p4: numpy.array,
                   position: numpy.array = numpy.array([0,0,0,1])) -> R3Object:
    V1 = Vertex(p1)
    V2 = Vertex(p2)
    V3 = Vertex(p3)
    V4 = Vertex(p4)
    vertexList = [V1,V2,V3,V4]
    
    faceList = []
    for i in range(len(vertexList)):
        faceList.append(Face([vertexList[i],vertexList[(i+1)%len(vertexList)],vertexList[(i+2)%len(vertexList)]],color=(50+i*50,50+i*50,50+i*50)))
    
    return R3Object(faceList,position)
        
       

   






            
