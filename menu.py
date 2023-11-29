import pygame as pg

import texthandling as th

import inputHandler


mainFont = "Comic Sans"

class Menu():
    def __init__(self, 
                 displaySurface: pg.surface) -> None:

        self.displaySurface = displaySurface

        self.mouseInputHandler = inputHandler.MouseInputHandler()



        
        self.textHandler = th.TextHandler(self.displaySurface,
                                          {
                                              "title":th.TextObject(mainFont,60,(255,255,255),"Memory3D",(300,150)),
                                              "byMe":th.TextObject(mainFont,30,(255,255,255),"By Isac Zobec ! !!!",(300,200)),
                                              "f":th.TextObject(mainFont,30,(255,255,255),"Memory3D",(300,250)),
                                          }
                                          )

    def Run(self):
        """Method that should be ran every frame the menu is active."""

        self.textHandler.RenderText("title")
        self.textHandler.RenderText("byMe")
        self.textHandler.RenderText("f")