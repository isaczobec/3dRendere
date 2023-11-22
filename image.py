import numpy as np
from numpy import array as ar
from PIL import Image
from typing import Dict

class PlaneImage():

    """Class that is used to project an image onto a plane."""

    def __init__(self,imagePath: str) -> None:
        self.imagePath = imagePath

        self.image = Image.open(self.imagePath)
        self.size = self.image.size

        self.pixels = self.image.load()

    def SampleRGB(self,x,y,scale = 1):
        """Returns the RGB-Value at the specefied position of the image."""
        return self.pixels[round(x * scale)%self.image.size[0],round(y * scale)%self.image.size[1]]
    

class ImageHandler():
    """Init takes a dict (reference string: file path) and creates a dict structured (references: planeImages). Used to render an image using a string stored in a 3d face."""
    def __init__(self,imagePathList: Dict[str,str]) -> None:

        self.planeImageDict = {}

        for ref,filePath in imagePathList.items():
            self.planeImageDict[ref] = PlaneImage(filePath)

    def GetImage(self,ref: str):
        """Gets the plane image from a reference string."""

        if ref != None:
            return self.planeImageDict[ref]
        else:
            return None
    
    
    






    




    


    

        


