import numpy as np
from numpy import array as ar
from PIL import Image

class PlaneImage():

    """Class that is used to project an image onto a plane."""

    def __init__(self,imagePath: str) -> None:
        self.imagePath = imagePath

        self.image = Image.open(self.imagePath)
        self.size = self.image.size

        self.pixels = self.image.load()

    def SampleRGB(self,x,y):
        """Returns the RGB-Value at the specefied position of the image."""
        return self.pixels[x,y]




    




    


    

        


