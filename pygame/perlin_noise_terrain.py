import random
import math

from colour import Color as Colour

from pixelPygame import PixelPygame, PixelMatrix

yellow = Colour("yellow")
green = Colour("green")
cyan = Colour("cyan")
blue = Colour("blue")

COLOR_RANGE_LENGTH = 20
land_colors = [c.hex_l for c in list(green.range_to(yellow, COLOR_RANGE_LENGTH))]
sea_colors = [c.hex_l for c in list(cyan.range_to(blue, COLOR_RANGE_LENGTH))]


class PerlinNoiseTerrain:
    def __init__(self, width, height):
        self.pixel_matrix = PixelMatrix(width, height)
        self.gradients = None

    def generate_terrain(self, blocks_per_x_axis=32):
        # gradients_per_x_axis = (self.pixel_matrix.get_width() // pixels_per_gradient_axis) + 1
        # gradients_per_y_axis = (self.pixel_matrix.get_height() // pixels_per_gradient_axis) + 1
        gradients_per_x_axis = blocks_per_x_axis + 1
        pixels_per_gradient_axis = self.pixel_matrix.get_width() // blocks_per_x_axis
        gradients_per_y_axis = (self.pixel_matrix.get_height() // pixels_per_gradient_axis) + 1

        self.gradients = [
            [(0.0, 0.0) for col in range(gradients_per_y_axis)]
            for row in range(gradients_per_x_axis)
        ]

        for row in range(gradients_per_x_axis):
            for col in range(gradients_per_y_axis):
                self.gradients[row][col] = self.random_gradient()

        for row in range((gradients_per_x_axis - 1) * pixels_per_gradient_axis):
            for col in range((gradients_per_y_axis - 1) * pixels_per_gradient_axis):
                x = row / pixels_per_gradient_axis
                y = col / pixels_per_gradient_axis

                perlin_value = 0
                sf = blocks_per_x_axis
                while sf >= 1:
                    perlin_value += self.perlin_noise(x, y, sf) * math.sqrt(sf)
                    sf //= 2

                perlin_value /= math.sqrt(blocks_per_x_axis)

                self.pixel_matrix.matrix[row][col] = self.get_elevation_color(perlin_value)

    def get_elevation_color(self, elevation_value):
        val = int(elevation_value * COLOR_RANGE_LENGTH)
        if val < 0:
            val = min(abs(val), COLOR_RANGE_LENGTH - 1)
            return sea_colors[val]
        else:
            val = min(val, COLOR_RANGE_LENGTH - 1)
            return land_colors[val]

    def perlin_noise(self, x: float, y: float, sf: int = 1):
        x = x / sf
        y = y / sf

        x0 = int(x)
        x1 = x0 + 1
        y0 = int(y)
        y1 = y0 + 1

        sx = x - x0
        sy = y - y0

        n0 = self.dot_grid_gradient(x0, y0, x, y, sf)
        n1 = self.dot_grid_gradient(x1, y0, x, y, sf)
        ix0 = self.interpolate(n0, n1, sx)

        n0 = self.dot_grid_gradient(x0, y1, x, y, sf)
        n1 = self.dot_grid_gradient(x1, y1, x, y, sf)
        ix1 = self.interpolate(n0, n1, sx)

        return self.interpolate(ix0, ix1, sy)

    def interpolate(self, a0: float, a1: float, w: float):
        # return (a1 - a0) * w + a0
        # return (a1 - a0) * (3.0 - w * 2.0) * w * w + a0
        return (a1 - a0) * ((w * (w * 6.0 - 15.0) + 10.0) * w * w * w) + a0

    def dot_grid_gradient(self, ix: int, iy: int, x: float, y: float, sf: int = 1):
        gradient_x, gradient_y = self.gradients[ix*sf][iy*sf]

        dx = x - ix
        dy = y - iy

        return dx*gradient_x + dy*gradient_y

    def random_gradient(self):
        rand_val = random.random() * (2 * math.pi)
        return math.sin(rand_val), math.cos(rand_val)


def main():
    pixel_pygame = PixelPygame("Procedurally Generated Terrain", 512, 512, 2.0)
    pixel_pygame.start(advance_game_state)


def advance_game_state():
    perlin_noise_terrain = PerlinNoiseTerrain(512, 512)     # TODO do this only once
    perlin_noise_terrain.generate_terrain()
    return perlin_noise_terrain.pixel_matrix.matrix


if __name__ == "__main__":
    main()
