import math

class Vector2:
    def __init__(self,x,y):
        self.x = x
        self.y = y

    def Normalize(self):
        if (self.x != 0 and self.y != 0):
            magnitude = math.sqrt(self.x**2 + self.y**2)
            self.x = self.x/magnitude
            self.y = self.y/magnitude

    def Magnitude(self):
        return math.sqrt(self.x**2 + self.y**2)
    
def Distance(point1: Vector2, point2 : Vector2) -> float:
    """returns the distance between two Vector2s"""
    return math.sqrt((point2.x - point1.x)**2 + (point2.y - point1.y)**2)



print(Distance(Vector2(-1,-1),Vector2(1,1)))