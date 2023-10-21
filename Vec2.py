import math

class Vec2:
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