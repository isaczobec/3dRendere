import pygame,settings
from Vec import Vector2 as Vec2



def GetMoveInputVector():
    keys = pygame.key.get_pressed()

    inputVector = Vec2(0,0)

    if keys[settings.keymap.get("up")]:
        inputVector.y -= 1
    if keys[settings.keymap.get("down")]:
        inputVector.y += 1
    if keys[settings.keymap.get("left")]:
        inputVector.x -= 1
    if keys[settings.keymap.get("right")]:
        inputVector.x += 1
    inputVector.Normalize()

    return inputVector

def GetTurnInputVector():
    keys = pygame.key.get_pressed()

    inputVector = Vec2(0,0)

    if keys[settings.keymap.get("turnup")]:
        inputVector.y -= 1
    if keys[settings.keymap.get("turndown")]:
        inputVector.y += 1
    if keys[settings.keymap.get("turnleft")]:
        inputVector.x -= 1
    if keys[settings.keymap.get("turnright")]:
        inputVector.x += 1
    inputVector.Normalize()

    return inputVector

def GetZoomInput() -> float:
    keys = pygame.key.get_pressed()

    returnInput = 0
    if keys[settings.keymap.get("zoomIn")]:
        returnInput -= 1
    if keys[settings.keymap.get("zoomOut")]:
        returnInput += 1

    return returnInput

def GetFlyInput() -> float:
    keys = pygame.key.get_pressed()

    returnInput = 0
    if keys[settings.keymap.get("flyUp")]:
        returnInput += 1
    if keys[settings.keymap.get("flyDown")]:
        returnInput -= 1

    return returnInput

class MouseInputHandler():
    """class for getting input from the players mouse"""

    def __init__(self) -> None:
        self.holdingClick = False

    def GetMouseInput(self):
        """Returns a tuple of the mouse position (converted from screen pixel position to canvas pixel position) if M1 was clicked this frame. Otherwise, returns null."""

        

        keys = pygame.key.get_pressed()
        if keys[settings.keymap.get("click")]:

            


            if self.holdingClick == False:

                pos = pygame.mouse.get_pos()

                self.holdingClick = True
                return [pos[0]/(settings.WIDTH/settings.PIXELXAMOUNT/2),(settings.HEIGHT - pos[1])/(settings.HEIGHT/settings.PIXELYAMOUNT/2)]
                

            self.holdingClick = True
            
        
        else:


            self.holdingClick = False
            return None


