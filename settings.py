import pygame

PIXELYAMOUNT,PIXELXAMOUNT = 360,640

HEIGHT,WIDTH = 720,1280

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

            "zoomIn":pygame.K_o,
            "zoomOut":pygame.K_l,
            
            "flyUp":pygame.K_x,
            "flyDown":pygame.K_c,

            }