import numpy
from virtualCamera import VirtualCamera 
import Objects3D as O3D
from Vec import Vector3 as V3
from math import cos,sin



class Renderer():
    def __init__(self,
                 camera = VirtualCamera(pitch = 0.1,yaw=1.3,position=V3(1,1,1))) -> None:
        
        self.camera = camera

        self.objectList = []
        """List of 3d objects that this renderer can render."""


    def GetNearClipCenter(self):
        fp = self.camera.position + self.camera.GetViewDirectionVector() * self.camera.nearClipPlaneDistance
        return fp



    def TransformPointByMatrix(self):
        """Gets the 4x4 matrix that will transform 3d space from the furstrum into the clip volume."""
        
        # furstrum point
        fp = self.GetNearClipCenter()

        # move the furstrums center to 0,0,0
        moveMatrix = numpy.array([[1,0,0,-fp.x],
                                 [0,1,0,-fp.y],
                                 [0,0,1,-fp.z],
                                 [0,0,0,1]])
        
        # rotate transform based on the cameras rotation, rotate it back to normal
        yaw = self.camera.yaw
        pitch = self.camera.pitch
        rotateYAxisArray = numpy.array([[cos(-yaw),0,sin(-yaw),0],
                                        [0,1,0,0],
                                        [-sin(-yaw),0,cos(-yaw),0],
                                        [0,0,0,1]])
        
        rotateXAxisArray = numpy.array([[1,0,0,0],
                                        [0,cos(-pitch),-sin(-pitch),0],
                                        [0,sin(-pitch),cos(-pitch),0],
                                        [0,0,0,1]])
        
        # might be some errors here based on order of multiplication maybe
        
        M = rotateXAxisArray @ rotateYAxisArray @ moveMatrix

        return M

        

        


renderer = Renderer()
matrix = renderer.TransformPointByMatrix()
print(str(renderer.camera.GetViewDirectionVector()))
print(matrix)

print(numpy.linalg.det(matrix))


nc = renderer.GetNearClipCenter()
transformed_nc = matrix @ numpy.array([nc.x, nc.y, nc.z, 1])
print(transformed_nc)

