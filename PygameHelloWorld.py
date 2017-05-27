import pygame, sys
from pygame.locals import *

# set up pygame
pygame.init()

# set up the window
windowSurface = pygame.display.set_mode((500,400), 0, 32)
pygame.display.set_caption('Hello World! (title bar)')

# set up the colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# # set up fonts
# basicFont = pygame.font.SysFont(None, 48)
#
# # set up the text
# text = basicFont.render('Hello World!', True, WHITE, BLUE)
# textRect = text.get_rect()
# textRect.centerx = windowSurface.get_rect().centerx
# textRect.centery = windowSurface.get_rect().centery
#
# # draw the white background onto the surface
# windowSurface.fill(WHITE)
#
# # draw a green polygon onto the surface
# pygame.draw.polygon(windowSurface, GREEN, ((146, 0), (291, 106), (236, 277),
#                                            (56, 277), (0, 106)))
# # draw some blue lines onto the surface
# pygame.draw.line(windowSurface, BLUE, (60, 60), (120, 60), 4)
# pygame.draw.line(windowSurface, BLUE, (120, 60), (60, 120))
# pygame.draw.line(windowSurface, BLUE, (60, 120), (120, 120), 4)
#
# # draw a blue circle onto the surface
# pygame.draw.circle(windowSurface, BLUE, (300, 50), 20, 0)
#
# # draw a red ellipse onto the surface
# pygame.draw.ellipse(windowSurface, RED, (300, 250, 40, 80), 1)
#
# # draw the text's background rectangle onto the surface
# pygame.draw.rect(windowSurface, RED, (textRect.left - 20, textRect.top - 20,
#                                       textRect.width + 40, textRect.height +40))
#
# # get a pixel array of the surface
# pixelArray = pygame.PixelArray(windowSurface)
# pixelArray[480][380] = BLACK
# del pixelArray
#
# # draw the text onto the surface
# windowSurface.blit(text, textRect)


def drawLine(windowSurface, color, startPos, endPos):
    pixelArray = pygame.PixelArray(windowSurface)

    slope =  float(endPos[1] - startPos[1]) / (endPos[0] - startPos[0])

    if slope < 1:
        for dx in xrange(endPos[0] - startPos[0] + 1):
            dy = int(round(dx * slope))
            pixelArray[startPos[0] + dx][startPos[1] + dy] = WHITE
    else:
        for dy in xrange(endPos[1] - startPos[1] + 1):
            if slope == 0:
                dx = 0
            else:
                dx = int(round(float(dy) / slope))
            pixelArray[startPos[0] + dx][startPos[1] + dy] = WHITE

    del pixelArray


windowSurface.fill(BLACK)
drawLine(windowSurface, WHITE, (10, 20), (462, 20))
pygame.draw.line(windowSurface, WHITE, (20, 10), (472, 10))

# draw the window onto the screen
pygame.display.update()

# run the game loop
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
