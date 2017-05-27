# This programs simulates, in a crude way, how water spreads out to fill the 
# space around it.

import pygame, sys, time
from pygame.locals import *

pygame.init()

windowSurface = pygame.display.set_mode((1000, 1000), 0, 32)
pygame.display.set_caption('WaterSim')

windowSurface.fill(255, 255, 255)

# construct array that defines the sequence of turns needed to construct a
# dragon curve of the desired order (state turns using cardinal directions?)

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    pygame.display.update()
    time.sleep(0.1)
    
    
"""
classes
    TileGrid
    Tile
    WaterTile
    
"""

class TileGrid:
    
    
class WaterTile:
    waterLevel;
    floorLevel;
    deltaWaterLevel;