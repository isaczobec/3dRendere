"""A module containing the pixel class."""

import settings
from Vec import Vector2
import pygame

class Pixel():
    """A pixel on the screen. Contains a color and a
    depthbuffer that is used to render polygons in the
    correct order."""
    def __init__(self,canvas,xpos,ypos,xCoord: int, yCoord: int,color=(0,0,0),depthBuffer: float = 1): # canvas is a class defined in canvas.py
        """Init this pixel. Create a pygame rect
        that is used to render this pixel."""

        self.canvas = canvas

        # calculate the size of this pixel, so that all pixels together will perfectly fit the screen
        pixelSizeX = settings.WIDTH / canvas.pixelAmountX
        pixelSizeY = settings.HEIGHT / canvas.pixelAmountY

        self.depthBuffer = depthBuffer

        self.pos = Vector2(xpos,ypos)
        self.rect = pygame.rect.Rect(self.pos.x,self.pos.y,pixelSizeX,pixelSizeY)
        self.color = color

        self.coordinates = Vector2(xCoord,yCoord)

    def Render(self,displaySurface) -> None:
        """Renders this pixele onto the displaysurface."""
        pygame.draw.rect(displaySurface,self.color,self.rect)