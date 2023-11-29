import numpy as np
from numpy import array as ar
from PIL import Image
from typing import Dict
import gameSettings

class PlaneImage():

    """Class that is used to project an image onto a plane."""

    def __init__(self,imagePath: str,
                 fitDimensions: tuple[float,float] = None # if the image should fit some dimensions in the world space, none if not
                 ) -> None:
        self.imagePath = imagePath

        self.image = Image.open(self.imagePath)
        self.size = self.image.size

        self.fitDimensions = fitDimensions
        

        self.pixels = self.image.load()

    def SampleRGB(self,x: float,y: float,
                  scale: tuple[float] = (1,1)):
        """Returns the RGB-Value at the specefied position of the image."""

        if self.fitDimensions == None:
            scaleFactor = (scale[0],scale[1])
        else:
            scaleFactor = (scale[0] * self.image.size[0]/self.fitDimensions[0],scale[1] * self.image.size[1]/self.fitDimensions[1])

        return self.pixels[round(x * scaleFactor[0])%self.image.size[0],round(y * scaleFactor[1])%self.image.size[1]]


class ImageHandler():
    """Init takes a dict (reference string: file path) and creates a dict structured (references: planeImages). UseYBB Md to render an image using a string stored in a 3d face."""
    def __init__(self,imagePathList: Dict[str,str], 
                 alphabetFitsPlanes: bool = True # if alphabet characters automatically should fit the default text card dimensions
                 ) -> None:

        self.planeImageDict = {}

        # generate a list of the alphabet
        alphabet = [chr(v) for v in range(ord('a'), ord('a') + 26)]
        alphabet.append("å")
        alphabet.append("ä")
        alphabet.append("ö")

        # create instances of the planeimage class
        for ref,filePath in imagePathList.items():
            
            if ref in alphabet and alphabetFitsPlanes == True: # 
                fitDimensions = (gameSettings.cardDimensionRatio[0]*-4.1/gameSettings.maxWordLength,gameSettings.cardDimensionRatio[1]) # the default dimensions for image cards
                print(ref,":",fitDimensions)
            else:
                fitDimensions = None

            self.planeImageDict[ref] = PlaneImage(filePath,fitDimensions=fitDimensions)

    def GetImage(self,ref: str):
        """Gets the plane image from a reference string."""

        if ref != None:
            return self.planeImageDict[ref]
        else:
            return None
        



