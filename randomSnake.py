# Animate color-changing snake slithers randomly across the screen

import pygame, sys, time, random
from pygame.locals import *

pygame.init()
random.seed()

# set up the colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
colors = [BLACK, RED, GREEN, BLUE]

LINE_LEN = 20

class LineSeg:
    def __init__(self, color, x1, y1, x2, y2, lineWidth):
        self.color = color
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.lineWidth = lineWidth

windowSurface = pygame.display.set_mode((60, 60), 0, 32)
screenWidth = windowSurface.get_width()
screenHeight = windowSurface.get_height()
pygame.display.set_caption('Dragon Curve Animation')

x1 = x2 = windowSurface.get_rect().centerx
y1 = y2 = windowSurface.get_rect().centery
x0 = x1 + LINE_LEN * random.choice((-1, 1))
y0 = y1 + LINE_LEN * random.choice((-1, 1))

line_list = [None]*5

i = 0
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    color = colors[(i // 4) % 4]

    dx0 = (x1 - x0) // LINE_LEN
    dy0 = (y1 - y0) // LINE_LEN
    next_pos_list = [(dx0, dy0)]
    if dx0 == 0:
        next_pos_list.append((1, dy0))
        next_pos_list.append((-1, dy0))
        next_pos_list.append((1, 0))
        next_pos_list.append((-1, 0))
    elif dy0 == 0:
        next_pos_list.append((dx0, 1))
        next_pos_list.append((dx0, -1))
        next_pos_list.append((0, 1))
        next_pos_list.append((0, -1))
    elif (x1 < LINE_LEN or (screenWidth - x1) < LINE_LEN) and (y1 < LINE_LEN or (screenHeight - y1) < LINE_LEN):
        next_pos_list = [(-dx0, 0), (0, -dy0)]
    else:
        next_pos_list.append((dx0, 0))
        next_pos_list.append((dx0, -dy0))
        next_pos_list.append((0, dy0))
        next_pos_list.append((-dx0, dy0))

    while True:
        dx, dy = random.choice(next_pos_list)
        x2_temp = x2 + LINE_LEN * dx
        y2_temp = y2 + LINE_LEN * dy
        if x2_temp < 0 or x2_temp > screenWidth or y2_temp < 0 or y2_temp > screenHeight:
            continue
        break

    x2 += LINE_LEN * dx
    y2 += LINE_LEN * dy

    line_list[i % 5] = LineSeg(color, x1, y1, x2, y2, 2)

    windowSurface.fill(WHITE)

    for x in range(1, 5 + 1):
        line = line_list[(i + x) % 5]
        if not line: continue
        pygame.draw.line(windowSurface, line.color, (line.x1, line.y1), (line.x2, line.y2), line.lineWidth)

    pygame.display.update()

    i += 1
    x0, y0 = x1, y1
    x1, y1 = x2, y2

    pygame.time.wait(100)
