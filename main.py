"""Main module of the memory game. Run this to run the game."""

import pygame
import time
import settings
import sys
from canvas import Canvas
from renderer import Renderer
import Time
import math
from game import GameManager
import menu

import cProfile
import pstats

# game states; different states the program can be in
menuState = "MENU" 
activeGameState = "GAME" 

class Application():
    """Main class. An instance is creates when the game in ran."""
    def __init__(self) -> None:
            """Init the main class. Initializes pygame and creates the display. Also
            creates references to the canvas, renderer and gamemanager."""

            # Initialize pygame and create the screen
            pygame.init()
            self.displaySurface = pygame.display.set_mode((settings.WIDTH,settings.HEIGHT))
            self.displaySurface.fill('black')
            pygame.display.set_caption("Very high production value game")
            self.clock = pygame.time.Clock()
            
            # capture the time of this frame
            self.lastFrameTime = time.time()

            # classes that are essential to run the game
            # theese are initialized when the game starts
            self.canvas: Canvas = None
            self.renderer: Renderer = None
            self.gameManager: GameManager = None

            self.menu = menu.Menu(self.displaySurface)

            self.gameState = menuState
            """Which state the game is currently in."""
            
            #self.polygon = Polygon([Vertex(50,50),Vertex(320,100),Vertex(321,200)],self.canvas)
            #self.polygon.DrawOutlinesWithEquations()
            #self.polygon.DrawOutlines()
            #print(self.polygon.bounds[0].x,self.polygon.bounds[0].y,self.polygon.bounds[1].x,self.polygon.bounds[1].y)
            #print(self.polygon.equationList)

            #self.slopeEquation = SlopeEquation(0.5,100,100,200)
            #self.slopeEquation.DrawSlopeLine(self.canvas)



    def run(self) -> None:
        """Run the game. Should be called every frame."""

        # The game loop
        while True:

            # if the player tries to exit the game, safely close the application
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return 

            # change the color of the background dynamically to cycle through all the colors of the rainbow (almost); very beautiful
            # purely cosmetic
            r = (math.sin(Time.passedTime * 0.5)+1) / 2 * 255
            g = (math.sin(Time.passedTime/3 * 0.5 + 6)+1) / 2 * 255
            b = (math.sin(Time.passedTime * 0.5 +23)+1) / 2 * 255
            self.displaySurface.fill((r,g,b))

            if self.gameState == menuState:
                self.RunMenu()

            elif self.gameState == activeGameState:
                self.RunActiveGame()

            # Calculate the deltatime this frame (deltatime = time between this frame and the last)
            Time.deltaTime = (time.time() - self.lastFrameTime)
            Time.passedTime += Time.deltaTime
            self.lastFrameTime = time.time()

            self.clock.tick(settings.MAXFPS) # limit the games FPS

            pygame.display.update() # update the display

    
    def RunMenu(self):
        """Runs the menu. Should be ran every frame that the menu is active."""
        self.menu.Run()
        if self.menu.gameRunning == True: 
            self.menu.menuMode == menu.mainMenuReference # set the menu mode to main menu so that the player gets back to there when they go back to the menu after the game
            self.StartActiveGame()
            
            
    def StartActiveGame(self) -> None:
        """Start the active memory game. Initializes the
        canvas, renderer and gamemanager."""

        print("Starting the game!")

        self.canvas = Canvas(self)
        self.renderer = Renderer(self.canvas)
        self.gameManager = GameManager(self.renderer,self.displaySurface)

        self.gameState = activeGameState

    def StopActiveGame(self) -> None:
        """Stops the memory game from running."""
        self.menu.gameRunning = False
        self.gameState = menuState

        self.menu.menuMode = menu.mainMenuReference

    def RunActiveGame(self):
        """Runs the game. Should be ran every frame that the game is active."""
        self.renderer.RenderScene()
        self.canvas.Refresh(self.displaySurface)
        self.gameManager.run()

        if self.gameManager.returnToMenu == True:
            self.StopActiveGame()




if __name__ == "__main__":

    # with cProfile.Profile() as profile:

    app = Application()
    app.run()

    pygame.quit()

    # results = pstats.Stats(profile)
    # results.sort_stats(pstats.SortKey.TIME)
    # results.print_stats()

    sys.exit()
    

            