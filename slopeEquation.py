"""Module with the SlopeEquation class"""

import settings
from Vec import Vector2

class SlopeEquation():
    """A class representing a slope equation (y = kx + m). 
    can be a horizontal/vertical line."""
    def __init__(self,
                 slope = 0,
                 offset = 0,
                 minXLimit = 0,
                 maxXLimit = settings.WIDTH) -> None:
        """Init the slopeEquation. Store the k and m values and its limits."""
        
        self.slope = slope
        self.offset = offset

        self.vertical = False
        self.xVerticalPosition = None

        self.minXLimit = minXLimit
        self.maxXLimit = maxXLimit

    def GetY(self,x):
        """returns the y postion of an x value using the slope equation."""
        y = self.slope * x + self.offset
        return y
    
    def AdjustToTwoPoints(self,
                          p1: Vector2,
                          p2: Vector2,
                          ) -> None:
        """Adjusts the k and m values of this slopequation to 
        intersect two given points."""

        deltaX = p1.x - p2.x
        deltaY = p1.y - p2.y

        
        if deltaX == 0: # make this slope vertical
            self.vertical = True
            self.slope = None
            self.xVerticalPosition = p1.x
            self.offset = None
        else: # calculate the slope and offset
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

        


    def GetIntersection(self,otherSlopeEquation) -> Vector2:
        """Gets the intersection (vector2(x,y)) between
        this slopeequation and another one."""
        
        
        if self.vertical == True:
            if otherSlopeEquation.vertical == True: # do not return any intersection if both lines are vertical
                return None

            x = self.xVerticalPosition
            y = otherSlopeEquation.GetY(x)
            return Vector2(x,y)
        elif otherSlopeEquation.vertical == True:
            x = otherSlopeEquation.xVerticalPosition
            y = self.GetY(x)
            return Vector2(x,y)

        try:
            # get the intersection from the two lines algebraicly
            x = (otherSlopeEquation.offset - self.offset)/(self.slope - otherSlopeEquation.slope)
            y = self.GetY(x)
        except ZeroDivisionError:
            return None

        # only return an intersection if the intersection is within the limits of both lines
        if x >= self.minXLimit and x <= self.maxXLimit and x >= otherSlopeEquation.minXLimit and x <= otherSlopeEquation.maxXLimit:

            return Vector2(x,y)
        
        else:
            return None


        #y = kx + m
        # k1x + m1 = k2x + m2
        # m2 - m1 = k1x - k2x
        # m2 - m1 = (k1-k2)x
        # (m2 - m1)/(k1-k2) = x