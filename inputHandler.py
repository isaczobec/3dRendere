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

    returnInput = 0;
    if keys[settings.keymap.get("zoomIn")]:
        returnInput += 1
    if keys[settings.keymap.get("zoomOut")]:
        returnInput -= 1

    return returnInput


