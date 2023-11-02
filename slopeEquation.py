import settings
from Vec import Vector2

class SlopeEquation():
    def __init__(self,slope = 0,offset = 0,minXLimit = 0,maxXLimit = settings.WIDTH):
        self.slope = slope
        self.offset = offset

        self.vertical = False
        self.xVerticalPosition = None

        self.minXLimit = minXLimit
        self.maxXLimit = maxXLimit

    def GetY(self,x):
        y = self.slope * x + self.offset
        return y
    
    def AdjustToTwoPoints(self,p1,p2):

        deltaX = p1.x - p2.x
        deltaY = p1.y - p2.y
        

        if deltaX == 0:
            self.vertical = True
            self.slope = None
            self.xVerticalPosition = p1.x
            self.offset = None
        else:
            self.slope = deltaY/deltaX
            self.offset = p1.y - self.slope * p1.x
            self.vertical = False
            self.xVerticalPosition = None


    def DrawSlopeLine(self,canvas,color = (255,255,255)):

        for n in range(self.maxXLimit - self.minXLimit):

            x = self.minXLimit + n
            
            y = self.GetY(x)

            if y <= settings.HEIGHT and y >= 0 and x <= settings.WIDTH and x >= 0:
                canvas.getPixel(x,round(y)).color = color

        


    def GetIntersection(self,otherSlopeEquation):

        
        if self.vertical == True:
            if otherSlopeEquation.vertical == True:
                return None

            x = self.xVerticalPosition
            y = otherSlopeEquation.GetY(x)
            return Vector2(x,y)
        elif otherSlopeEquation.vertical == True:
            x = otherSlopeEquation.xVerticalPosition
            y = self.GetY(x)
            return Vector2(x,y)

        try:
            x = (otherSlopeEquation.offset - self.offset)/(self.slope - otherSlopeEquation.slope)
            y = self.GetY(x)
        except ZeroDivisionError:
            return None

        if x >= self.minXLimit and x <= self.maxXLimit and x >= otherSlopeEquation.minXLimit and x <= otherSlopeEquation.maxXLimit:

            return Vector2(x,y)
        
        else:
            return None


        #y = kx + m
        # k1x + m1 = k2x + m2
        # m2 - m1 = k1x - k2x
        # m2 - m1 = (k1-k2)x
        # (m2 - m1)/(k1-k2) = x