import random
import math
import queue

import numpy as np

from pixelPygame import PixelPygame, PixelMatrix


class MyColor:
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    FOREST_GREEN = (31, 93, 65)
    SEA_GREEN = (81, 135, 89)
    DARK_KHAKI = (152, 171, 99)
    BLUE = (0, 0, 255)
    ROYAL_BLUE = (75.0, 87.0, 215.0)
    LIGHT_STEEL_BLUE = (159, 193, 242)
    CORN_FLOWER_BLUE = (118, 142, 234)

    
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
    

class LakeProGen:
    def __init__(self, width, height):
        self.pixel_matrix = PixelMatrix(width, height, MyColor.GREEN)

    def generate_fractal_lake(self):
        # pick four corners with some randomness
        center_width = self.pixel_matrix.get_width() // 2
        center_height = self.pixel_matrix.get_height() // 2
        center_point = Point(center_width, center_height)
        a = center_width // 2
        b = a * 3
        rand_position_factor = center_width // 5
        
        point2 = self.randomPoint(Point(b, a), rand_position_factor)
        point1 = self.randomPoint(Point(a, a), rand_position_factor)
        point3 = self.randomPoint(Point(a, b), rand_position_factor)
        point4 = self.randomPoint(Point(b, b), rand_position_factor)

        self.pixel_matrix.set_pixel_color(point1, MyColor.BLUE)
        self.pixel_matrix.set_pixel_color(point2, MyColor.BLUE)
        self.pixel_matrix.set_pixel_color(point3, MyColor.BLUE)
        self.pixel_matrix.set_pixel_color(point4, MyColor.BLUE)
        
        # recursively add midpoints along sides
        self.createFractalEdge(point1, point2)
        self.createFractalEdge(point2, point4)
        self.createFractalEdge(point4, point3)
        self.createFractalEdge(point3, point1)
        
        self.fillFromPoint(center_point, MyColor.BLUE)

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

    def createFractalEdge(self, point1, point2, color=MyColor.BLUE):
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
        
        self.pixel_matrix.set_pixel_color(point_mid, color)
        self.createFractalEdge(point1, point_mid, color)
        self.createFractalEdge(point_mid, point2, color)

    def randomRound(self, float):  
        if float.as_integer_ratio()[1] == 2:
            roundedAsFloat = math.floor(float + random.randint(0, 1))
            return int(roundedAsFloat)

        return int(np.rint(float))

    def fillFromPoint(self, point, fillColor):
        pointQueue = queue.Queue()
        
        oldColor = self.pixel_matrix.get_pixel_color(point)
        self.pixel_matrix.set_pixel_color(point, fillColor)
        pointQueue.put(point)
        
        while not pointQueue.empty():
            point = pointQueue.get()
            for pt in point.getNeighborList():
                if self.shouldBeFilled(pt, oldColor):
                    self.pixel_matrix.set_pixel_color(pt, fillColor)
                    pointQueue.put(pt)

    def shouldBeFilled(self, point, oldColor):
        pointColor = self.pixel_matrix.get_pixel_color(point)
        if pointColor == oldColor:
            return True
            
        return False


def main():
    pixel_pygame = PixelPygame("Procedurally Generated Lake", 512, 512, 2.0)
    pixel_pygame.start(advance_game_state)


def advance_game_state():
    lake_pro_gen = LakeProGen(256, 256)
    lake_pro_gen.generate_fractal_lake()
    return lake_pro_gen.pixel_matrix.matrix
        
        
if __name__ == "__main__":
    main()
