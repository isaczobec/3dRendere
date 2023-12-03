"""Module containing classes that
make up a 3d object. has classes for vertexes,
faces and full 3d objects."""

import numpy
from typing import List
from math import cos,sin,acos,asin,atan,pi
from image import PlaneImage
from virtualCamera import VirtualCamera
import copy


class Vertex():
    """A single vertex in space, with a position
    stored. Makes up faces."""
    def __init__(self,
            position: numpy.array = numpy.array([0,0,0,1])) -> None:
        """Store this vertex's position and normal."""
        
        self.position = position
        """The position in the worldspace (numpy.array([x,y,z,w])) of this vertex.
        The 4th dimension coordinate should always be 1 as it is soley used to move
        vertecies using matrix transforms."""

        self.normal: numpy.ndarray = None # !! Unused in the final game
        """The normal (numpy.array([x,y,z])) stored in this vertex. Used
        to calculate smooth lighting and such."""

        
        

class Face():
    """A face in 3d space. Contains a list
    of vertecies which makes up a polygon."""
    def __init__(self,vertexList: List[numpy.array], # list of vertexes making up this plane
                 color: (float,float,float) = (255,255,255), 
                 planeImage: PlaneImage = None, # the planeImage to render onto this face
                 planeImageScale: float = (1,1), # The scale at which the plane image is rendered
                 virtualCamera: VirtualCamera = None,
                 imageTransformMatrix = None,
                 enabled = True, # if this face should be rendered or not
                 flipNormal = False
                ) -> None: # how man image points this plane should have; which resolution it should render with
        """Init this face. Stores its values inside it."""

        self.vertexList = vertexList
        self.color = color


        self.planeImage = planeImage
        self.planeImageScale = planeImageScale
        self.virtualCamera = virtualCamera
        self.imageTransformMatrix = imageTransformMatrix
        self.enabled = enabled

        self.flipNormal = flipNormal

        
    def GetImageTransformMatrix(self,debug = False) -> numpy.ndarray:
        """Returns a 4x4 numpy matrix that transforms coordinates
        on this face to an x,y position that can be used to sample
        the color of an image. Moves the first vertex of this polygon
        to 0,0,0. Reverses the furstrum to view volume
        transform. Only works on triangles or straight quads."""

        #Needs a reference to the camera to get the scaling factor (difference between near and far clip plane)
        if self.virtualCamera != None:

            # copy this face as it needs to be partially transformed to calculate some values
            copyFace = copy.deepcopy(self)

            # scale back to the original size on the z-axis
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

            # get normal vector for this plane
            nV = copyFace.GetNormalVector()
            if debug: print("original normal vector: ",nV)
            
            # the forward vector, the direction we want the plane to be facing (To get z = 0 for all points on this plane)
            fV = numpy.array([0,0,1]) 

            # angle between the two vectors
            ang = acos((numpy.dot(nV,fV)) / (numpy.linalg.norm(fV) * numpy.linalg.norm(nV)))
            if debug: print("ang:",ang)

            if ang != 0: # do not do a rotation transform if the polygons normal is already facing the right way. also stops a mathematical error

                # rotation axis, perpendicular to both nV and fV
                rA = numpy.cross(nV,fV)
                rA = rA / numpy.linalg.norm(rA)

                if debug: print("rotation axis:",rA)

                # copied this matrix from wikipedia (by hand D: ) (https://en.wikipedia.org/wiki/Rotation_matrix)
                # This matrix rotates a point ang radians on the rA vector (rA has to be a unit vector)
                rotationMatrix = numpy.array([
                                            [cos(ang) + ((rA[0]**2) * (1-cos(ang))), (rA[0] * rA[1] * (1-cos(ang)))-(rA[2]*sin(ang)), rA[0]*rA[2]*(1-cos(ang))+rA[1]*sin(ang),0],
                                            [rA[1]*rA[0]*(1-cos(ang))+rA[2]*sin(ang), cos(ang)+ rA[1]**2 * (1-cos(ang)), rA[1]*rA[2]*(1-cos(ang))-rA[0]*sin(ang),0],
                                            [rA[2]*rA[0]*(1-cos(ang)) - rA[1]*sin(ang), rA[2]*rA[1]*(1-cos(ang))+rA[0]*sin(ang), cos(ang) + rA[2]**2 * (1-cos(ang)),0],
                                            [0,0,0,1]
                                            ])

                # apply the rotation matrix, needs to be done to correctly calculate the move matrix
                for vertex in copyFace.vertexList:
                    vertex.position = rotationMatrix @ vertex.position

            else: # if we dont need to rotate the face, the rotation matrix is an identity matrix
                rotationMatrix = numpy.array([
                                                [1,0,0,0],
                                                [0,1,0,0],
                                                [0,0,1,0],
                                                [0,0,0,1],
                                              ])

            # How much we need to move the 
            firstVertexOffset = copyFace.vertexList[0].position

            # matrix that will move the first vertex in the polygon to 0,0,0
            moveMatrix = numpy.array([
                                        [1,0,0,-firstVertexOffset[0]],
                                        [0,1,0,-firstVertexOffset[1]],
                                        [0,0,1,-firstVertexOffset[2]],
                                        [0,0,0,1],
                                         ])
            

            # matrix to rotate the polygon to be straight; if the camera was turned the images were rotated
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

            # Multiply all the matrixes so far
            matrix = rotateToCameraMatrix @ moveMatrix @ rotationMatrix @ scalingMatrix

            v1pos = matrix @ self.vertexList[1].position

            # get the angle betwen straight up and the second vertex
            angToUp = -1 * numpy.arctan(v1pos[1]/v1pos[0])

            # rotation matrix so that the second vertex always is always straight above the first vertex; so that the image gets rotated properly
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
        """Divides this face into triangles if it is a quad. 
        returns a list of triangle faces. If not a quad, 
        return a list of only this face."""

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
        """returns a 4 dimensional vector (numpy.array([x,y,z,a])), where the first 3 numbers is 
        the normal vector of the plane. The 4th, a, is the right 
        hand side of the equation."""

        basePoint = self.vertexList[0].position

        planeNormalVector = self.GetNormalVector()

        # calculate what the right hand side of the planes equation should be, based on the fact that the base point should be on the plane
        equationResult = planeNormalVector[0] * basePoint[0] + planeNormalVector[1] * basePoint[1] + planeNormalVector[2] * basePoint[2]

        equationVector = numpy.array([planeNormalVector[0],planeNormalVector[1],planeNormalVector[2],equationResult])

        return equationVector
    
    def GetNormalVector(self):
        """Gets the normal vector (numpy.array([x,y,z])) of this face. flips it
        if this face has flipped normals."""

        point1Vector: numpy.array = self.vertexList[1].position - self.vertexList[0].position
        point2Vector: numpy.array = self.vertexList[-1].position - self.vertexList[0].position

        # Cross the two vectors to get a normal that is perpendicular to them both
        # Cannot cross 4d vectors, so convert them to 3d
        planeNormalVector = numpy.cross(numpy.array([point1Vector[0],point1Vector[1],point1Vector[2]]),numpy.array([point2Vector[0],point2Vector[1],point2Vector[2]]))

        planeNormalVector = planeNormalVector / numpy.linalg.norm(planeNormalVector) # normalize the vector

        if self.flipNormal:
            return planeNormalVector * -1
        else:
            return planeNormalVector



        

class R3Object():
    """three-dimensional object consisting of a list of faces."""
    def __init__(self, 
                 faceList: list[Face], 
                 position: numpy.array, 
                 rotation: numpy.array = numpy.array([0,0,0]), 
                 triangulate: bool = False,
                 enabled = True, # if the object should be rendered
                 hasVertexNormals: bool = False, # if this object should store information of vertex normals
                 renderSmooth: bool = False, # if this polygon should be rendered smoothly
                 ) -> None:
        """Takes a list of faces and creates a 3d object from them.
        Also creates a linear list of all its vertecies."""

        self.faceList: List[Face] = []

        # if we want to triangulate every face in this object:
        if triangulate == True:
            self.TriangulateAllFaces(faceList)
        else:
            self.faceList = faceList

        self.enabled = enabled

        self.vertexList: List[Vertex] = self.CreateVertexList()

        self.position = position

        # variables associated with smooth shading.
        # Unused in final game
        self.renderSmooth = renderSmooth
        self.hasVertexNormals = hasVertexNormals
        if self.hasVertexNormals:
            self.CalculateVertexNormals()

        # Rotate this object to the specefied rotation
        self._rotation = rotation
        self.Rotate(rotation[0],rotation[1],rotation[2])

    def TriangulateAllFaces(self, faceList) -> None:
        """Triangulate all faces in this object and
        append the resulting triangles to this object's
        facelist."""
        for face in faceList: # iterate through all faces and append all the triangulated faces to this objects faceList.
            for triangulatedFace in face.Triangulate():
                self.faceList.append(triangulatedFace)

    def CreateVertexList(self) -> list[Vertex]:
        """Creates and returns a linear list of vertexes for this object."""
        vertexList = []
        for face in self.faceList:
            if face != None: # Do not create a vertex list from faces that are disabled
                for vertex in face.vertexList:
                    if vertex not in vertexList:
                        vertexList.append(vertex)
        return vertexList

    def CalculateVertexNormals(self) -> None:
        """Calculate all vertex normals (numpy.array([x,y,z])) 
        for this polygon and store them in each vertex."""

        vertexStoredNormals: dict[Vertex:list[numpy.ndarray]] = {}
        for vertex in self.vertexList:
            vertexStoredNormals[vertex] = [] # add empty lists for all vertexes

        for face in self.faceList:
            faceNormal = face.GetNormalVector()
            for vertex in face.vertexList: 
                vertexStoredNormals[vertex].append(faceNormal)
            
        for vertex,normalList in vertexStoredNormals.items():
            averageVector = numpy.array([0,0,0])
            for normal in normalList:
                averageVector = averageVector + normal

            averageVector = averageVector / len(normalList)

            averageVector = averageVector / numpy.linalg.norm(averageVector) # normalize the normal

            vertex.normal = averageVector

    
    def Move(self,
             x:float,y:float,z:float) -> None:
        """Move this polygon using matrix multiplication."""
        
        moveMatrix =numpy.array([[1,0,0,x],
                                 [0,1,0,y],
                                 [0,0,1,z],
                                 [0,0,0,1]])
        self.position = moveMatrix @ self.position

    
    def Rotate(self,x: float,y: float,z: float, 
               degrees = True): # if the input is in degrees or radians
        """Rotate this vector said degrees/radians on every respective axis."""

        if degrees:
            # convert radians to degrees
            x = x * pi/180
            y = y * pi/180
            z = z * pi/180
        
        # create rotation matricies on all axises
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

        # create 3x3 matricies for rotating 3d normal vectors, 4x4 matricies can not be applied on them
        # unused in the final game
        if self.hasVertexNormals:
            normalXMatrix = numpy.array([[1,0,0],
                                [0,cos(x),-sin(x)],
                                [0,sin(x),cos(x)],
                                ])
            
            normalYMatrix = numpy.array([[cos(y),0,sin(y)],
                                [0,1,0],
                                [-sin(y),0,cos(y)],
                                ])

            normalZMatrix = numpy.array([
                                [cos(z),-sin(z),0],
                                [sin(z),cos(z),0],
                                [0,0,1],
                                ])


        # apply the rotation to all verticies
        for vertex in self.vertexList:
            vertex.position = XMatrix @ vertex.position
            vertex.position = YMatrix @ vertex.position
            vertex.position = ZMatrix @ vertex.position
    
            if self.hasVertexNormals:
                vertex.normal = normalXMatrix @ vertex.normal
                vertex.normal = normalYMatrix @ vertex.normal
                vertex.normal = normalZMatrix @ vertex.normal

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



    
        


        
        

def CreateTetrahedron(p1: numpy.ndarray,
                   p2: numpy.ndarray,
                   p3: numpy.ndarray,
                   p4: numpy.ndarray,
                   position: numpy.ndarray = numpy.array([0,0,0,1]),
                   renderSmooth: bool = False
                   ) -> R3Object:
    """Creates and returns a tetrahedron (R3Object) with corners on every specefied point."""
    # !!! not really a part of the memory game, just made this to test the renderer!!!!!!
    V1 = Vertex(p1)
    V2 = Vertex(p2)
    V3 = Vertex(p3)
    V4 = Vertex(p4)
    vertexList = [V1,V2,V3,V4]
    
    faceList = []
    for i in range(len(vertexList)):
        # create a face between this verticies and the two next in the vertex list
        faceList.append(Face([vertexList[i],vertexList[(i+1)%len(vertexList)],vertexList[(i+2)%len(vertexList)]]))
    
    return R3Object(faceList,position,renderSmooth=renderSmooth,hasVertexNormals=renderSmooth)


def CreateUVSphere(radius: float = 1, 
                   segments: int = 32, 
                   rings: int = 16, 
                   position: numpy.ndarray = numpy.array([0,0,0,1]),
                   color: tuple[float] = (255,255,255),

                   triangulateFaces: bool = True, # if the spheres faces should be triangulated
                   renderSmooth: bool = False,
                   virtualCamera: VirtualCamera = None # the virtualcamera of the faces. used for rendering images or smooth shading
                   ) -> R3Object:
    """Creates and returns a UV sphere (R3Object) with the
    specefied radius and amount of segments and rings."""
    # !!! not really a part of the memory game, just made this to test the renderer!!!!!!

    ringStep = pi/rings # the difference in angle between each ring
    segmentStep = 2*pi/segments # the difference in angle between each segment
    
    # create the top and bottom verticies
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
                    ],color=color,virtualCamera=virtualCamera))
                
            elif ringIndex == rings - 1: # if this is the last ring, also add triangles
                faceList.append(Face([
                    ringVertList[segmentIndex], # add this vertex to the face
                    ringVertList[(segmentIndex+1)%len(ringVertList)], # add the next vertex to the face
                    ringList[ringIndex-1][(segmentIndex+1)%len(ringVertList)], # add the face 
                    ringList[ringIndex-1][segmentIndex],

                    ],color=color,virtualCamera=virtualCamera))
                
                faceList.append(Face([
                    ringVertList[segmentIndex], # add this vertex to the face
                    ringVertList[(segmentIndex+1)%len(ringVertList)], # add the next vertex to the face
                    botVert
                    ],flipNormal=True,color=color,virtualCamera=virtualCamera))
                

            else:

                faceList.append(Face([
                    ringVertList[segmentIndex], # add this vertex to the face
                    ringVertList[(segmentIndex+1)%len(ringVertList)], # add the next vertex to the face
                    ringList[ringIndex-1][(segmentIndex+1)%len(ringVertList)], # add the face 
                    ringList[ringIndex-1][segmentIndex],

                    ],color=color,virtualCamera=virtualCamera))
                
    UVsphere = R3Object(faceList=faceList,position=position,triangulate=triangulateFaces,hasVertexNormals=renderSmooth,renderSmooth=renderSmooth)

    return UVsphere
        









    





        
       








            
