import pygame

PIXELYAMOUNT,PIXELXAMOUNT = 90,160

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

            "zoomIn":pygame.K_c,
            "zoomOut":pygame.K_x,
            
            "flyUp":pygame.K_SPACE,
            "flyDown":pygame.K_LSHIFT,

            "click":pygame.K_b

            }