import numpy as np

class RenderingInformation():
    """Class that contains information used
    every frame for rendering."""
    def __init__(self,sunLightDirection: np.ndarray,
                 sunColor: tuple,
                 sunCap: float,
                 cameraDirectionVector: np.ndarray
                 ) -> None:
        """Init the renderinginformation class. Stores all passsed in arguments."""

        self.sunLightDirection = sunLightDirection
        """the direction (x,y,z) the sun light is coming from. Should be normalized."""
        self.sunCap = sunCap
        """The minimum value of the sun factor."""
        self.sunColor = sunColor
        """The color of the sun in rgb values."""

        self.cameraDirectionVector = cameraDirectionVector
        """The direction (x,y,z) the camera is viewing in the world space. normalized."""
        