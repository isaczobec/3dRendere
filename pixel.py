import settings
from Vec import Vector2
import pygame

class Pixel():
    def __init__(self,canvas,xpos,ypos,xCoord: int, yCoord: int,color=(0,0,0)): # canvas is a class defined in canvas.py

        self.canvas = canvas

        pixelSizeX = settings.WIDTH / canvas.pixelAmountX
        pixelSizeY = settings.HEIGHT / canvas.pixelAmountY


    

        self.pos = Vector2(xpos,ypos)
        self.rect = pygame.rect.Rect(self.pos.x,self.pos.y,pixelSizeX,pixelSizeY)
        self.color = color

        self.coordinates = Vector2(xCoord,yCoord)

    def Render(self,displaySurface):
        pygame.draw.rect(displaySurface,self.color,self.rect)