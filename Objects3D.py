from Vec import Vector3 as V3
import numpy
from typing import List
from math import cos,sin,acos,asin,atan,pi
from image import PlaneImage
from virtualCamera import VirtualCamera
import copy


class Vertex():
    def __init__(self,
            position: numpy.array = numpy.array([0,0,0,1])) -> None:
        
        self.position = position
        

class Face():
    def __init__(self,vertexList: List[numpy.array], # list of vertexes making up this plane
                 color: (float,float,float) = (255,255,255), 
                 planeImage: PlaneImage = None, # the planeImage to render onto this face
                 planeImageScale: float = (100,100), # The scale at which the plane image is rendered
                 virtualCamera: VirtualCamera = None,
                 imageTransformMatrix = None,
                 enabled = True, # if this face should be rendered or not
                 flipNormal = False
                ) -> None: # how man image points this plane should have; which resolution it should render with

        self.vertexList = vertexList
        self.color = color


        self.planeImage = planeImage
        self.planeImageScale = planeImageScale
        self.virtualCamera = virtualCamera
        self.imageTransformMatrix = imageTransformMatrix
        self.enabled = enabled

        self.flipNormal = flipNormal

        
    def GetImageTransformMatrix(self,debug = False):

        #Needs a reference to the camera to get the scaling factor (difference between near and far clip plane)
        if self.virtualCamera != None:

            copyFace = copy.deepcopy(self)



            scalingFactor = 1/(copyFace.virtualCamera.GetScalingFactor())
            


            scalingMatrix = numpy.array([
                                        [1,0,0,0],
                                        [0,1,0,0],
                                        [0,0,scalingFactor,0],
                                        [0,0,0,1],
                                         ])
            


            #needs to do this before calculating the rotation matrix because the normal vector will be different
            for vertex in copyFace.vertexList:
                vertex.position = scalingMatrix @ vertex.position

            # normal vector for this plane
            nV = copyFace.GetNormalVector()
            if debug: print("original normal vector: ",nV)
            
            # the forward vector, the direction we want the plane to be facing
            fV = numpy.array([0,0,1]) # the vector the normal vector should be facing after 

            # angle between the two vectors
            ang = acos((numpy.dot(nV,fV)) / (numpy.linalg.norm(fV) * numpy.linalg.norm(nV)))
            if debug: print("ang:",ang)

            if ang != 0: # do not do a rotation transform if the polygons normal is already facing the right way. also stops a mathematical error

                # rotation axis, perpendicular to both nV and fV
                rA = numpy.cross(nV,fV)
                rA = rA / numpy.linalg.norm(rA)

                if debug: print("rotation axis:",rA)

                # copied this matrix from wikipedia (by hand D: ) (https://en.wikipedia.org/wiki/Rotation_matrix)
                rotationMatrix = numpy.array([
                                            [cos(ang) + ((rA[0]**2) * (1-cos(ang))), (rA[0] * rA[1] * (1-cos(ang)))-(rA[2]*sin(ang)), rA[0]*rA[2]*(1-cos(ang))+rA[1]*sin(ang),0],
                                            [rA[1]*rA[0]*(1-cos(ang))+rA[2]*sin(ang), cos(ang)+ rA[1]**2 * (1-cos(ang)), rA[1]*rA[2]*(1-cos(ang))-rA[0]*sin(ang),0],
                                            [rA[2]*rA[0]*(1-cos(ang)) - rA[1]*sin(ang), rA[2]*rA[1]*(1-cos(ang))+rA[0]*sin(ang), cos(ang) + rA[2]**2 * (1-cos(ang)),0],
                                            [0,0,0,1]
                                            ])

                # apply the rotation matrix, needs to be done to correctly calculate the move matrix
                
                for vertex in copyFace.vertexList:
                    vertex.position = rotationMatrix @ vertex.position

            else:
                rotationMatrix = numpy.array([
                                                [1,0,0,0],
                                                [0,1,0,0],
                                                [0,0,1,0],
                                                [0,0,0,1],
                                              ])


            firstVertexOffset = copyFace.vertexList[0].position

            # matrix that will move the first vertex in the polygon to 0,0,0
            moveMatrix = numpy.array([
                                        [1,0,0,-firstVertexOffset[0]],
                                        [0,1,0,-firstVertexOffset[1]],
                                        [0,0,1,-firstVertexOffset[2]],
                                        [0,0,0,1],
                                         ])
            

            
            


            # matrix to rotate the polygon to be straight
            zAngle = -self.virtualCamera.yaw
            rotateToCameraMatrix = numpy.array([
                                                [cos(zAngle),-sin(zAngle),0,0],
                                                [sin(zAngle),cos(zAngle),0,0],
                                                [0,0,1,0],
                                                [0,0,0,1]
                                                ])
                                                

            
            if debug: 
                print("new normal vector:",copyFace.GetNormalVector())
            
                print("New vertex positions:")
                for vertex in copyFace.vertexList:
                    print(vertex.position)

            # the finished matrix we want to return
            matrix = rotateToCameraMatrix @ moveMatrix @ rotationMatrix @ scalingMatrix

            v1pos = matrix @ self.vertexList[1].position


            # Rotate the matrix so that the second vertex always is straight above the 
            angToUp = -1 * numpy.arctan(v1pos[1]/v1pos[0])

            rotateToStraightMatrix = numpy.array([
                                                [cos(angToUp),-sin(angToUp),0,0],
                                                [sin(angToUp),cos(angToUp),0,0],
                                                [0,0,1,0],
                                                [0,0,0,1]
                                                ])
            matrix = rotateToStraightMatrix @ matrix

            if debug: 
                print("finnished matrix:")
                print(matrix)

                print("transformed vertex positions:")
                for vertex in self.vertexList:
                    print(matrix @ vertex.position)
            


            

            return matrix

        else:
            print("This plane needs a reference to a camera to get the image transform matrix!") 




        




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

        
        # Cannot cross 4d vectors
        planeNormalVector = numpy.cross(numpy.array([point1Vector[0],point1Vector[1],point1Vector[2]]),numpy.array([point2Vector[0],point2Vector[1],point2Vector[2]]))

        planeNormalVector = planeNormalVector / numpy.linalg.norm(planeNormalVector) # normalize the vector

        

        if self.flipNormal:
            return planeNormalVector * -1
        else:
            return planeNormalVector



        

class R3Object():
    """three-dimensional object consisting of a bunch of vertexes. Created by inputting a list of Faces."""
    def __init__(self, 
                 faceList: List[Face], 
                 position: numpy.array, 
                 rotation: numpy.array = numpy.array([0,0,0]), 
                 triangulate: bool = False,
                 enabled = True, # if the object should be rendered
                 ) -> None:

        self.faceList: List[Face] = []

        # if we want to triangulate every face in this object:
        if triangulate == True:
            for face in faceList: # iterate through all faces and append all the triangulated faces to this objects faceList.
                for triangulatedFace in face.Triangulate():
                    self.faceList.append(triangulatedFace)
        else:
            self.faceList = faceList

        self.enabled = enabled

        self.vertexList: List[Vertex] = self.CreateVertexList()

        self.position = position

        self._rotation = rotation
        self.Rotate(rotation[0],rotation[1],rotation[2])
        

    def CreateVertexList(self):
        """Creates and returns a linear list of vertexes for this object."""
        vertexList = []
        for face in self.faceList:
            if face != None: # Do not create a vertex list from faces that are disabled
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

    
    def Rotate(self,x: float,y: float,z: float, 
               degrees = True): # if the input is in degrees or radians
        """Rotate this vector said radians on every respective axis."""

        if degrees:
            
            x = x * pi/180
            y = y * pi/180
            z = z * pi/180
        
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
    
    def Update(self):
        """Function that can be overrided in child classes. Ran every frame in the renderer class."""
        pass

    def ObjectClicked(self):
        """Function that is called in the game class when this object is clicked. Overrided in child classes."""
        self.Rotate(5,0,0)

    def __deepcopy__(self,memo):
        """Override the deepcopy method. Only copy this object if it is enabled and only copy the faces that are enabled."""

        if self.enabled == True:

            copiedFaces = []
            for face in self.faceList: 
                if face.enabled == True:
                    copiedFaces.append(copy.deepcopy(face))
                else:
                    copiedFaces.append(None)
                    
            return R3Object(copiedFaces,self.position)
        else:
            return None



    
        


        
        

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
        faceList.append(Face([vertexList[i],vertexList[(i+1)%len(vertexList)],vertexList[(i+2)%len(vertexList)]]))
    
    return R3Object(faceList,position)


def CreateUVSphere(radius: float = 1, 
                   segments: int = 32, 
                   rings: int = 16, 
                   position: numpy.ndarray = numpy.array([0,0,0,1]),
                   
                   ) -> R3Object:
    """Creates and returns a UV sphere."""

    ringStep = pi/rings # the difference in angle between each ring
    segmentStep = 2*pi/segments # the difference in angle between each segment
    
    topVert = Vertex(numpy.array([0,radius,0,1]))
    botVert = Vertex(numpy.array([0,-radius,0,1]))

    
    faceList: List[Face] = []

    ringList: List[List[Vertex]] = [[topVert]] # the top vertex is the first ring


    # add the square faces in the middle of the sphere
    for ringIndex in range(1,rings):
        ringVertList: List[Vertex] = []


        for segmentIndex in range(segments):

            ringVertList.append(Vertex(numpy.array([cos(segmentIndex*segmentStep)*sin((ringIndex)*ringStep)*radius,cos((ringIndex)*ringStep)*radius,sin(segmentIndex*segmentStep)*sin((ringIndex)*ringStep)*radius,1])))

        ringList.append(ringVertList)

        for segmentIndex in range(segments):

            if ringIndex == 1: # if the triangle faces should be added; this is the top ring
                faceList.append(Face([
                    ringVertList[segmentIndex], # add this vertex to the face
                    ringVertList[(segmentIndex+1)%len(ringVertList)], # add the next vertex to the face
                    topVert
                    ]))
                
            elif ringIndex == rings - 1: # if this is the last ring, add triangles
                print("HEJ")
                faceList.append(Face([
                    ringVertList[segmentIndex], # add this vertex to the face
                    ringVertList[(segmentIndex+1)%len(ringVertList)], # add the next vertex to the face
                    botVert
                    ]))
                

            else:

                faceList.append(Face([
                    ringVertList[segmentIndex], # add this vertex to the face
                    ringVertList[(segmentIndex+1)%len(ringVertList)], # add the next vertex to the face
                    ringList[ringIndex-1][(segmentIndex+1)%len(ringVertList)], # add the face 
                    ringList[ringIndex-1][segmentIndex],

                    ]))
                
    UVsphere = R3Object(faceList=faceList,position=position)

    return UVsphere
        


for i in range(1,10-1):
    print(i)







    





        
       








            
