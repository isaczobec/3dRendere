"""Module containing setting variables used in 
the program, including the resolution of 
the canvas and the screen. Also contains a 
changeable keymap for the players input."""
import pygame

PIXELYAMOUNT,PIXELXAMOUNT = 180,320

HEIGHT,WIDTH = 720,1280

MAXFPS = 30

keymap = {
            
            "up":pygame.K_w,
            "left":pygame.K_a,
            "right":pygame.K_d,
            "down":pygame.K_s,
            "slow":pygame.K_SPACE,
            "turnup":pygame.K_UP,
            "turnleft":pygame.K_LEFT,
            "turnright":pygame.K_RIGHT,
            "turndown":pygame.K_DOWN,

            "zoomIn":pygame.K_c,
            "zoomOut":pygame.K_x,
            
            "flyUp":pygame.K_SPACE,
            "flyDown":pygame.K_LSHIFT,

            "click":pygame.K_b,
            "exit":pygame.K_p,

            }