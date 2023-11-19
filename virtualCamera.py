from Vec import Vector3 as V3
import math
import inputHandler
import Time

class VirtualCamera():
    def __init__(self,
            aspectRatio = [1.6,0.9],
            nearClipPlaneDistance: float = 1,
            farClipPlaneDistance: float = 100,
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


        self.zoomFactor = 3
        """How fast the camera changes aspect ratio"""

        self.flyUpFactor = 5
        """How fast the camera flies up"""

        self.moveFactor = 5
        """How fast the camera moves through wasd"""

        self.turnFactor = 1.75
        """How fast the camera turns"""

    def GetViewDirectionVector(self) -> V3:

        #x = math.cos(self.pitch) * math.cos(self.yaw)
        #y = math.sin(self.pitch)
        #z = math.cos(self.pitch) * math.sin(self.yaw)


        x = math.cos(-self.yaw) * math.cos(-self.pitch)
        y = math.sin(-self.pitch)
        z = math.sin(-self.yaw) * math.cos(-self.pitch)

        returnVector = V3(x,y,z)
        returnVector.Normalize()
        return returnVector
    
    def GetPerpMovementVector(self) -> V3:
        z = -math.cos(self.yaw)
        x = -math.sin(self.yaw)
        
        returnVector = V3(x,0,z)
        returnVector.Normalize()
        return returnVector
    


    def MoveCamera(self):
        moveInputVector = inputHandler.GetMoveInputVector() * Time.deltaTime * self.moveFactor
        vv = self.GetViewDirectionVector()
        

        #self.position.z -= moveInputVector.x
        #self.position.x -= moveInputVector.y
        self.position += self.GetPerpMovementVector() * moveInputVector.x
        self.position -= vv * moveInputVector.y
        

        turnInputVector = inputHandler.GetTurnInputVector() * Time.deltaTime * self.turnFactor
        self.yaw += turnInputVector.x
        self.pitch += turnInputVector.y

        zoomInput = inputHandler.GetZoomInput()
        self.aspectRatio[0] *= (1 + zoomInput * self.zoomFactor * Time.deltaTime)
        self.aspectRatio[1] *= (1 + zoomInput * self.zoomFactor * Time.deltaTime)

        self.position.y += inputHandler.GetFlyInput() * self.flyUpFactor * Time.deltaTime


    def GetScalingFactor(self):
        """Get the factor by which the clip volume needs to be scaled to have a depth of 1"""
        return 1/(self.farClipPlaneDistance-self.nearClipPlaneDistance)
        
    
        
    
virtualCamera = VirtualCamera()
print(virtualCamera.GetViewDirectionVector())
        

        
        



