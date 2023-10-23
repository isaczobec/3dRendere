import math

class Vector2:
    def __init__(self,x,y):
        self.x = x
        self.y = y

    def Normalize(self):
        magnitude = math.sqrt(self.x**2 + self.y**2)
        if magnitude != 0:
            self.x = self.x/magnitude
            self.y = self.y/magnitude


    def Magnitude(self):
        return math.sqrt(self.x**2 + self.y**2)
    
    def Add(self, 
            otherVector): # the vector which is to be added to this one
        """Adds another vector to this one"""
        self.x += otherVector.x
        self.y += otherVector.y

    
    
def Distance(point1: Vector2, point2 : Vector2) -> float:
    """returns the distance between two Vector2s"""
    return math.sqrt((point2.x - point1.x)**2 + (point2.y - point1.y)**2)


zero = Vector2(0,0) # constant vector, usefull for quicker and cleaner usage

def Add(vector1: Vector2, vector2: Vector2) -> Vector2:
    """returns the sum of two vectors"""
    returnVector = Vector2(vector1.x+vector2.x,vector1.y+vector2.y)
    return returnVector

def Multiply(vector: Vector2, scalar: float) -> Vector2:
    """Returns the inputted vector multiplied by the inputted float"""
    return Vector2(vector.x * scalar, vector.y * scalar)