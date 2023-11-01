from Vec import Vector3 as V3
from typing import List

class Vertex():
    def __init__(self,
            position = V3(0,0,0)) -> None:
        
        self.position = position

class Face():
    def __init__(self,vertexList: List[Vertex]) -> None:

        self.vertexList = vertexList;

class R3Object():
    """three-dimensional object consisting of a bunch of vertexes. Created by inputting a list of Faces."""
    def __init__(self, faceList: List[Face]) -> None:

        self.faceList = faceList

        self.vertexList = self.CreateVertexList()

    def CreateVertexList(self):
        vertexList = []
        for face in self.faceList:
            for vertex in face.vertexList:
                if vertex not in vertexList:
                    vertexList.append(vertex)
        return vertexList
        


        
        

def CreateTetrahedron(p1: V3,
                   p2: V3,
                   p3: V3,
                   p4: V3) -> R3Object:
    V1 = Vertex(p1)
    V2 = Vertex(p2)
    V3 = Vertex(p3)
    V4 = Vertex(p4)
    vertexList = [V1,V2,V3,V4]
    
    faceList = []
    for i in range(len(vertexList)):
        faceList.append(Face([vertexList[i],vertexList[(i+1)%len(vertexList)],vertexList[(i+2)%len(vertexList)]]))
    
    return R3Object(faceList)
        
       

   

CreateTetrahedron = CreateTetrahedron(V3(1,1,1),V3(2,2,2),V3(0,1,0),V3(0,1,0))




            
