import pygame, sys
from pygame.locals import *
from pixelPygame import drawPixelMatrix


class Color():
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)

    
class PixelBalls():
    @classmethod
    def main(cls):
        pygame.init()

        surface = pygame.display.set_mode((400,200), 0, 32)
        pygame.display.set_caption('Hello World! (title bar)')
        
        while True:
            cls.advanceGameState(surface)    
            cls.handlePygameEvents()
            pygame.time.wait(100)
                
                
    @staticmethod
    def advanceGameState(surface):
        pixelMatrix = [[Color.GREEN, Color.RED, Color.BLUE, Color.WHITE],
                           [Color.RED, Color.WHITE, Color.RED, Color.GREEN]]
                            
        drawPixelMatrix(surface, pixelMatrix)

        pygame.display.update()

        
    @staticmethod
    def handlePygameEvents():
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            
            
# beginning of script
PixelBalls().main()
