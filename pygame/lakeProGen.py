import pygame, sys, random, math, queue, time
import numpy as np
from pygame.locals import *
from pixelPygame import drawPixelMatrix


class Color:
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    
    
class Point:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
        self.rightNeighbor = None
        self.leftNeighbor = None
        self.upperNeighbor = None
        self.lowerNeighbor = None
        self.neighborList = []
        
    def getRightNeighbor(self):
        if not self.rightNeighbor:
            self.rightNeighbor = Point(self.x+1, self.y)
        return self.rightNeighbor
        
    def getLeftNeighbor(self):
        if not self.leftNeighbor:
            self.leftNeighbor = Point(self.x-1, self.y)
        return self.leftNeighbor
        
    def getUpperNeighbor(self):
        if not self.upperNeighbor:
            self.upperNeighbor = Point(self.x, self.y+1)
        return self.upperNeighbor
        
    def getLowerNeighbor(self):
        if not self.lowerNeighbor:
            self.lowerNeighbor = Point(self.x, self.y-1)
        return self.lowerNeighbor
        
    def getNeighborList(self):
        if not self.neighborList:
            self.neighborList.append(self.getRightNeighbor())
            self.neighborList.append(self.getLeftNeighbor())
            self.neighborList.append(self.getUpperNeighbor())
            self.neighborList.append(self.getLowerNeighbor())
        return self.neighborList
        
    def isSameAsOrNextTo(self, point):
        return abs(self.x - point.x) <= 1 and abs(self.y - point.y) <= 1
        
        
class PixelMatrix:
    def __init__(self, pixelMatrix):
        self.matrix = pixelMatrix
        
        
    def getWidth(self):
        return len(self.matrix[0])
        
        
    def getHeight(self):
        return len(self.matrix)
        
        
    def setPixelColor(self, point, color=Color.BLUE):
        if point.x < 0 or point.y < 0:
            return
    
        try:
            self.matrix[point.y][point.x] = color
        except IndexError:
            pass
        
    
    def getPixelColor(self, point):
        if point.x < 0 or point.y < 0:
            return None
    
        try:
            return self.matrix[point.y][point.x]
        except IndexError:
            return None
    
	
class LakeProGen:
    def __init__(self, pixelMatrix):
        self.pixelMatrix = PixelMatrix(pixelMatrix)
            
    
    def generateFractalLake(self):
        #self.pixelMatrix.setPixelColor(Point(25, 25), Color.RED)
        
        # pick four corners with some randomness
        centerWidth = self.pixelMatrix.getWidth() // 2
        centerHeight = self.pixelMatrix.getHeight() // 2
        centerPoint = Point(centerWidth, centerHeight)
        a = centerWidth // 2
        b = a * 3
        randPositionFactor = centerWidth // 5
        
        point2 = self.randomPoint(Point(b, a), randPositionFactor)
        point1 = self.randomPoint(Point(a, a), randPositionFactor)
        point3 = self.randomPoint(Point(a, b), randPositionFactor)
        point4 = self.randomPoint(Point(b, b), randPositionFactor)
        
        # x1 = a + random.randint(rand_min, rand_max)
        # x2 = b + random.randint(rand_min, rand_max)
        # x3 = a + random.randint(rand_min, rand_max)
        # x4 = b + random.randint(rand_min, rand_max)
        
        # y1 = a + random.randint(rand_min, rand_max)
        # y2 = a + random.randint(rand_min, rand_max)
        # y3 = b + random.randint(rand_min, rand_max)
        # y4 = b + random.randint(rand_min, rand_max)
        
        
        self.pixelMatrix.setPixelColor(point1, Color.BLUE)
        self.pixelMatrix.setPixelColor(point2, Color.BLUE)
        self.pixelMatrix.setPixelColor(point3, Color.BLUE)
        self.pixelMatrix.setPixelColor(point4, Color.BLUE)
        
        # recursively add midpoints along sides
        self.createFractalEdge(point1, point2)
        self.createFractalEdge(point2, point4)
        self.createFractalEdge(point4, point3)
        self.createFractalEdge(point3, point1)
        
        self.fillFromPoint(centerPoint, Color.BLUE)
        
        
    def randomPoint(self, point, x, y=None, x_n=None, y_n=None):
        x = abs(x)
        if not y: 
            y = x
        if not x_n: 
            x_n = -x
        if not y_n: 
            y_n = -y 
        
        new_point = Point()
        new_point.x = point.x + random.randint(x_n, x)
        new_point.y = point.y + random.randint(y_n, y)
        
        return new_point
        
        
    def createFractalEdge(self, point1, point2, color=Color.BLUE):
        if point1.isSameAsOrNextTo(point2):
            return
    
        point_mid = Point()
        point_mid.x = self.randomRound((point1.x + point2.x) / 2.0)
        point_mid.y = self.randomRound((point1.y + point2.y) / 2.0)
        
        skewFactor = 0.4
        
        y_skew_max = self.randomRound(abs(point1.x - point2.x) * skewFactor)
        x_skew_max = self.randomRound(abs(point1.y - point2.y) * skewFactor)
        
        point_mid.x = point_mid.x + random.randint(-x_skew_max, x_skew_max)
        point_mid.y = point_mid.y + random.randint(-y_skew_max, y_skew_max)
        
        self.pixelMatrix.setPixelColor(point_mid, color)
        self.createFractalEdge(point1, point_mid, color)
        self.createFractalEdge(point_mid, point2, color)
        
        
    def randomRound(self, float):  
        if float.as_integer_ratio()[1] == 2:
            roundedAsFloat = math.floor(float + random.randint(0, 1))
            return int(roundedAsFloat)

        return int(np.rint(float))
        

    def fillFromPoint(self, point, fillColor):
        pointQueue = queue.Queue()
        
        oldColor = self.pixelMatrix.getPixelColor(point)
        self.pixelMatrix.setPixelColor(point, fillColor)
        pointQueue.put(point)
        
        while not pointQueue.empty():
            point = pointQueue.get()
            for pt in point.getNeighborList():
                if self.shouldBeFilled(pt, oldColor):
                    self.pixelMatrix.setPixelColor(pt, fillColor)
                    pointQueue.put(pt)
        
        
    def shouldBeFilled(self, point, oldColor):
        pointColor = self.pixelMatrix.getPixelColor(point)
        if pointColor == oldColor:
            return True
            
        return False
    
        '''pointColor = self.pixelMatrix.getPixelColor(point)
        if pointColor == color or pointColor == None:
            return
            
        self.pixelMatrix.setPixelColor(point, color)
        
        top_neighbor = Point(point.x, point.y+1)
        bottom_neighbor = Point(point.x, point.y-1)
        left_neighbor = Point(point.x-1, point.y)
        right_neighbor = Point(point.x+1, point.y)
        
        self.fillFromPoint(top_neighbor, color)
        self.fillFromPoint(bottom_neighbor, color)
        self.fillFromPoint(left_neighbor, color)
        self.fillFromPoint(right_neighbor, color)'''
        
        
    '''def fillFromPoint(self, point, color):
        pointColor = self.pixelMatrix.getPixelColor(point)
        if pointColor == color or pointColor == None:
            return
            
        self.pixelMatrix.setPixelColor(point, color)
        
        top_neighbor = Point(point.x, point.y+1)
        bottom_neighbor = Point(point.x, point.y-1)
        left_neighbor = Point(point.x-1, point.y)
        right_neighbor = Point(point.x+1, point.y)
        
        self.fillFromPoint(top_neighbor, color)
        self.fillFromPoint(bottom_neighbor, color)
        self.fillFromPoint(left_neighbor, color)
        self.fillFromPoint(right_neighbor, color)'''
    
    

def main():
    pygame.init()

    surface = pygame.display.set_mode((500,500), 0, 32)
    pygame.display.set_caption('Procedurally Generated Lake')
    
    #cls.advanceGameState(surface)   
    while True:
        t = time.process_time()
        advanceGameState(surface)
        print(time.process_time() - t, 's')
        for times in range(0,20):
            handlePygameEvents()
            pygame.time.wait(100)


def advanceGameState(surface):
    width, height = 250, 250
    # switch to numpy ndarrays for better performance?
    pixelMatrix = [[Color.GREEN for col in range(0, width)] 
                    for row in range(0,height)]
    lakeProGen = LakeProGen(pixelMatrix)
    lakeProGen.generateFractalLake()
                        
    drawPixelMatrix(surface, lakeProGen.pixelMatrix.matrix)

    pygame.display.update()
    
    
def handlePygameEvents():
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        
        
# Beginning of Script
main()    