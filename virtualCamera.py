"""a module containing the virtualcamera class."""

from Vec import Vector3 as V3
import math
import inputHandler
import Time

class VirtualCamera():
    """A class representing the virtual camera used
    to render the scene. Has variables that create a
    view furstrum which is transformed by the renderer class
    to render all 3d objects."""
    def __init__(self,
            aspectRatio = [1.6,0.9],
            nearClipPlaneDistance: float = 1,
            farClipPlaneDistance: float = 100,
            position = V3(0,0,0),
            pitch = 0,
            yaw = 0) -> None:
        """Init the virtualcamera. Set all its attributes."""

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
        """Returns a normalized direction vector facing
        the same way as the camera is."""

        #x = math.cos(self.pitch) * math.cos(self.yaw)
        #y = math.sin(self.pitch)
        #z = math.cos(self.pitch) * math.sin(self.yaw)

        # calculate the x,y,z values from the camera's pitch and yaw
        x = math.cos(-self.yaw) * math.cos(-self.pitch)
        y = math.sin(-self.pitch)
        z = math.sin(-self.yaw) * math.cos(-self.pitch)

        returnVector = V3(x,y,z)
        returnVector.Normalize()
        return returnVector
    
    def GetPerpMovementVector(self) -> V3:
        """Returns a normalized vector that faces to the side of the camera."""
        
        z = -math.cos(self.yaw)
        x = -math.sin(self.yaw)
        
        returnVector = V3(x,0,z)
        returnVector.Normalize()
        return returnVector
    


    def MoveCamera(self) -> None:
        """Moves this camera based on the players input.
        Ran every frame. Takes time between frames into account
        for consistent motion."""

        
        moveInputVector = inputHandler.GetMoveInputVector() * Time.deltaTime * self.moveFactor # get the players inputted movement vector and multiply it with the deltatime

        vv = self.GetViewDirectionVector()

        self.position += self.GetPerpMovementVector() * moveInputVector.x # move the camera from the players horizontal input
        self.position -= vv * moveInputVector.y # move the camera from the players vertical input
        
        # turn the camera around
        turnInputVector = inputHandler.GetTurnInputVector() * Time.deltaTime * self.turnFactor
        self.yaw += turnInputVector.x
        self.pitch += turnInputVector.y

        # Zoom in or out by scaling the cameras aspect ratio
        zoomInput = inputHandler.GetZoomInput()
        self.aspectRatio[0] *= (1 + zoomInput * self.zoomFactor * Time.deltaTime)
        self.aspectRatio[1] *= (1 + zoomInput * self.zoomFactor * Time.deltaTime)

        # Fly up or down
        self.position.y += inputHandler.GetFlyInput() * self.flyUpFactor * Time.deltaTime


    def GetScalingFactor(self):
        """Get the factor by which the clip volume needs to be scaled to have a depth of 1"""
        return 1/(self.farClipPlaneDistance-self.nearClipPlaneDistance)
        
        
    
        

        
        



