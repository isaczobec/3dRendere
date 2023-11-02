from Vec import Vector3 as V3
import math

class VirtualCamera():
    def __init__(self,
            aspectRatio = (16,9),
            nearClipPlaneDistance: float = 1,
            farClipPlaneDistance: float = 10,
            position = V3(0,0,0),
            pitch = 0,
            yaw = 0) -> None:

        self.position = position
        self.pitch = pitch
        """in radians."""
        self.yaw = yaw
        """in radians."""
        
        self.aspectRatio = aspectRatio
        self.nearClipPlaneDistance = nearClipPlaneDistance
        self.farClipPlaneDistance = farClipPlaneDistance

    def GetViewDirectionVector(self) -> V3:
        x = math.cos(self.pitch) * math.cos(self.yaw)
        y = math.sin(self.pitch)
        z = math.cos(self.pitch) * math.sin(self.yaw)
        returnVector = V3(x,y,z)
        returnVector.Normalize()
        return returnVector
    
        
    
virtualCamera = VirtualCamera()
print(virtualCamera.GetViewDirectionVector())
        

        
        



