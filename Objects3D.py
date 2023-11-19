from Vec import Vector3 as V3
import numpy
from typing import List
from math import cos,sin
from image import PlaneImage

class Vertex():
    def __init__(self,
            position: numpy.array = numpy.array([0,0,0])) -> None:
        
        self.position = position
        

class Face():
    def __init__(self,vertexList: List[numpy.array], # list of vertexes making up this plane
                 color: (float,float,float) = (255,255,255), 
                 planeImage: PlaneImage = None, # the planeImage to render onto this face
                 ) -> None: # how man image points this plane should have; which resolution it should render with

        self.vertexList = vertexList
        self.color = color


        self.planeImage = planeImage




        




    def Triangulate(self):
        """Divides this face into triangles if it is a quad. returns a list of triangle faces. If not a quad, return a list of only this face."""

        triangleFaceList = []

        if len(self.vertexList) == 4: # if this Face/polygon is a square
            
            # Split the list into two triangles and append each to the list:
            triangleFaceList.append(Face(self.vertexList[0:3],color=self.color))
            self.vertexList.pop(1) # removes the second vertex to that the remaining three will be connected
            triangleFaceList.append(Face(self.vertexList,color=self.color))


            return triangleFaceList
        
        else:
            return [self]
        


    def GetPlaneEquation(self) -> numpy.array:
        """returns a 4 dimensional vector, where the first 3 numbers is the normal vector of the plane. The 4th is the right hand side of the equation."""

        basePoint = self.vertexList[0].position
        

        planeNormalVector = self.GetNormalVector()

        # calculate what the right hand side of the planes equation should be, based on the fact that the base point should be on the plane
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
    def __init__(self, faceList: List[Face], position: numpy.array, rotation: numpy.array = numpy.array([0,0,0]), triangulate: bool = True) -> None:

        self.faceList = []

        # if we want to triangulate every face in this object:
        if triangulate == True:
            for face in faceList: # iterate through all faces and append all the triangulated faces to this objects faceList.
                for triangulatedFace in face.Triangulate():
                    self.faceList.append(triangulatedFace)
        else:
            self.faceList = faceList

        self.vertexList: List[Vertex] = self.CreateVertexList()

        self.position = position

        self._rotation = rotation
        self.Rotate(rotation[0],rotation[1],rotation[2])
        

    def CreateVertexList(self):
        """Creates and returns a linear list of vertexes for this object."""
        vertexList = []
        for face in self.faceList:
            for vertex in face.vertexList:
                if vertex not in vertexList:
                    vertexList.append(vertex)
        return vertexList
    
    def Move(self,
             x,y,z):
        """Move this polygon using matrix multiplication."""
        
        moveMatrix =numpy.array([[1,0,0,x],
                                 [0,1,0,y],
                                 [0,0,1,z],
                                 [0,0,0,1]])
        self.position = moveMatrix @ self.position

    
    def Rotate(self,x: float,y: float,z: float):
        """Rotate this vector said radians on every respective axis."""
        
        XMatrix = numpy.array([[1,0,0,0],
                               [0,cos(x),-sin(x),0],
                               [0,sin(x),cos(x),0],
                               [0,0,0,1]])
        
        YMatrix = numpy.array([[cos(y),0,sin(y),0],
                               [0,1,0,0],
                               [-sin(y),0,cos(y),0],
                               [0,0,0,1]])

        ZMatrix = numpy.array([
                               [cos(z),-sin(z),0,0],
                               [sin(z),cos(z),0,0],
                               [0,0,1,0],
                               [0,0,0,1]
                               ])
        
        for vertex in self.vertexList:
            vertex.position = XMatrix @ vertex.position
            vertex.position = YMatrix @ vertex.position
            vertex.position = ZMatrix @ vertex.position
        


        
        

def CreateTetrahedron(p1: numpy.array,
                   p2: numpy.array,
                   p3: numpy.array,
                   p4: numpy.array,
                   position: numpy.array = numpy.array([0,0,0,1])) -> R3Object:
    """Creates and returns a tetrahedron with corners on every specefied point."""
    V1 = Vertex(p1)
    V2 = Vertex(p2)
    V3 = Vertex(p3)
    V4 = Vertex(p4)
    vertexList = [V1,V2,V3,V4]
    
    faceList = []
    for i in range(len(vertexList)):
        faceList.append(Face([vertexList[i],vertexList[(i+1)%len(vertexList)],vertexList[(i+2)%len(vertexList)]],color=(50+i*50,50+i*50,50+i*50)))
    
    return R3Object(faceList,position)
        
       

   






            
