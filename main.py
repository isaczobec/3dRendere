import pygame
import time
import settings
import sys
from canvas import Canvas
from slopeEquation import SlopeEquation
from polygon import Polygon,Vertex
from Vec import Vector2
from renderer import Renderer
import Time
import math
import numpy
from game import GameManager

import cProfile
import pstats

class Game():
    def __init__(self):

            pygame.init()
            self.displaySurface = pygame.display.set_mode((settings.WIDTH,settings.HEIGHT))
            self.displaySurface.fill('black')
            pygame.display.set_caption("Very high production value game")
            self.clock = pygame.time.Clock()
            
            self.deltaTime = 0

            self.lastFrameTime = time.time()

            self.canvas = Canvas(self)

            self.renderer = Renderer(self.canvas)
            self.gameManager = GameManager(self.renderer,self.displaySurface)
            
            #self.polygon = Polygon([Vertex(50,50),Vertex(320,100),Vertex(321,200)],self.canvas)
            #self.polygon.DrawOutlinesWithEquations()
            #self.polygon.DrawOutlines()
            #print(self.polygon.bounds[0].x,self.polygon.bounds[0].y,self.polygon.bounds[1].x,self.polygon.bounds[1].y)
            #print(self.polygon.equationList)

            #self.slopeEquation = SlopeEquation(0.5,100,100,200)
            #self.slopeEquation.DrawSlopeLine(self.canvas)




    def run(self):

        #Spel-loopen
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return

            r = (math.sin(Time.passedTime * 0.5)+1) / 2 * 255
            g = (math.sin(Time.passedTime/3 * 0.5 + 6)+1) / 2 * 255
            b = (math.sin(Time.passedTime * 0.5 +23)+1) / 2 * 255
            self.displaySurface.fill((r,g,b))

            #self.polygon.DrawFilled()

            #self.canvas.DrawCircle(Vector2(100,100),10)

            self.RunActiveGame()
            
            Time.deltaTime = (time.time() - self.lastFrameTime)
            Time.passedTime += Time.deltaTime
            self.lastFrameTime = time.time()



            # print("FPS:",1/self.deltaTime)
            # print("Time between frames:",Time.deltaTime)
            
            self.clock.tick(30)

            #updatera skärmen och med intervaller bestämda av spelets fps
            pygame.display.update()

    


    def RunActiveGame(self):
        self.renderer.RenderScene()
        self.canvas.Refresh(self.displaySurface)
        self.gameManager.run()



if __name__ == "__main__":

    # with cProfile.Profile() as profile:

    game = Game()
    game.run()

    pygame.quit()

    # results = pstats.Stats(profile)
    # results.sort_stats(pstats.SortKey.TIME)
    # results.print_stats()

    sys.exit()
    

            