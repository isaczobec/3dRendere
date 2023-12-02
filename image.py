"""Module with classes used for rendering images
on 3d planes."""

from PIL import Image
import gameSettings
import errorHandling as EH



class PlaneImage():
    """Class that is used to project an image onto a plane."""

    def __init__(self,imagePath: str,
                 fitDimensions: tuple[float,float] = None # if the image should fit some dimensions in the world space, none if not
                 ) -> None:
        """Init this class. Opens and loads the specefied image."""

        self.imagePath = imagePath
        self.fitDimensions = fitDimensions

        self.image = EH.HandleExceptions(Image.open,[self.imagePath],errorMessage="The image file could not be opened!") 
        self.size = self.image.size

        self.pixels = self.image.load()

    def SampleRGB(self,x: float,y: float,
                  scale: tuple[float] = (1,1)) -> tuple[float,float,float]:
        """Returns the RGB-Value at the specefied position of the image."""

        if self.fitDimensions == None:
            scaleFactor = (scale[0],scale[1])
        else:
            scaleFactor = (scale[0] * self.image.size[0]/self.fitDimensions[0],scale[1] * self.image.size[1]/self.fitDimensions[1])

        return self.pixels[round(x * scaleFactor[0])%self.image.size[0],round(y * scaleFactor[1])%self.image.size[1]]


class ImageHandler():
    """Class used for storing references to PlaneImages and rendering
    accesing them easily. 
    Init takes a dict (reference string: file path) and creates 
    a dict structured (references: planeImages). 
    UseYBB Md to render an image using a string stored in a 3d face."""
    def __init__(self,imagePathList: dict[str,str], 
                 alphabetFitsPlanes: bool = True # if alphabet characters automatically should fit the default text card dimensions
                 ) -> None:
        """takes a dict (reference string: file path) and creates 
        a dict structured (references: planeImages)."""

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

    def GetImage(self,ref: str) -> PlaneImage:
        """Gets the plane image from a reference string."""
        if ref != None:
            return self.planeImageDict[ref]
        else:
            return None
        



