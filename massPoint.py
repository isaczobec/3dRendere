from Vec2 import Vector2
import Vec2

        

class MassPoint():
    """An object which serves as a point which springs can be connected between, used for softbody physics"""
    def __init__(self,position: Vector2, velocity: Vector2 = Vector2(0,0), force: Vector2 = Vector2(0,0), mass: float = 1, gravityVector: Vector2 = Vector2(0,-0)) -> None:

        self.position = position
        self.velocity = velocity
        self.force = force
        self.mass = mass
        self.gravityVector = gravityVector

        self.springList = []
        
    def Connect(self,massPoint) -> None:
        """Connects this masspoint to the inputted MassPoint by creating a Spring object between them."""
        self.springList.append(Spring(self,massPoint,setRestLength=True,restLength=45))

    def Update(self, deltaTime:float) -> None:
        """Updates all forces and values of this MassPoint"""

        self.force = Vec2.zero # set force to zero. Is to be calculated each frame

        self.force.Add(self.gravityVector) # adds gravity to force
    
        self.force.Add(self.GetSpringForce())

        self.velocity.Add(Vec2.Multiply(Vec2.Multiply(self.force,deltaTime),1/self.mass)) # adds the force divided by mass (F/m = a) multiplied by the deltatime to the velocity
        self.position.Add(Vec2.Multiply(self.velocity,deltaTime)) # adds the velocity multiplied by the deltatime to the position

    def GetSpringForce(self) -> Vector2:
        """Calculates the spring force acting on this MassPoint based on which other MassPoints it is attached to"""

        totalSpringForce = Vec2.zero

        for spring in self.springList:

            directionVector = Vec2.Add(spring.massPoint2.position,Vec2.Multiply(spring.massPoint1.position,-1))
            directionVector.Normalize()


            # Calculate the spring force using hooke's law: 
            localSpringForceMagnitude = (Vec2.Distance(spring.massPoint1.position,spring.massPoint2.position) - spring.restLength) * spring.stiffness 
            
            
            localSpringForceVector = Vec2.Multiply(directionVector,localSpringForceMagnitude)

            totalSpringForce.Add(localSpringForceVector)
            print(totalSpringForce.x,totalSpringForce.y)

        return totalSpringForce

        


class Spring():
    """Spring which is connected between two MassPoints. Used to calculate spring force between them."""
    def __init__(self, massPoint1:MassPoint, massPoint2:MassPoint, setRestLength: bool = False, restLength: float = 1, stiffness: float = 2, dampingFactor: float = 1) -> None:
        
        self.massPoint1 = massPoint1
        self.massPoint2 = massPoint2

        self.stiffness = stiffness

        if setRestLength == True:
            self.restLength = restLength
        # Set the restLength to the distance between the masspoints when the spring was created
        else:
            self.restLength = Vec2.Distance(massPoint1.position,massPoint2.position)

        self.dampingFactor = dampingFactor
