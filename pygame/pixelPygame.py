import sys
import time
from collections.abc import Callable

import pygame
from pygame.locals import *


def handle_pygame_events():
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()


class PixelPygame:
    def __init__(self, window_title: str, surface_width: int, surface_height: int, frame_duration_s: float = 1.0):
        pygame.init()
        self.frame_duration_s = frame_duration_s
        self.surface = pygame.display.set_mode((surface_width, surface_height), 0, 32)
        pygame.display.set_caption(window_title)

    def start(self, advance_game_state: Callable):
        image_num = 0
        next_update_time = None
        is_frame_ready = False
        while True:
            if not is_frame_ready:
                t = time.process_time()

                pixel_matrix = advance_game_state()
                self.draw_pixel_matrix(pixel_matrix)
                is_frame_ready = True

                frame_draw_duration = time.process_time() - t
                print(f"Frame draw took {frame_draw_duration} s")
                # pygame.image.save(surface, f"perlin-noise-terrain-{image_num}.jpg")
                # image_num += 1

            handle_pygame_events()
            if next_update_time is None or next_update_time < time.time():
                pygame.display.update()
                is_frame_ready = False
                next_update_time = time.time() + self.frame_duration_s
            else:
                pygame.time.wait(100)

    def draw_pixel_matrix(self, pixel_matrix):
        """
        :param pixel_matrix: unragged list of lists of pygame colors
        Prerequisites:
        #     - Pygame needs to already have been initialized
        #     - Every row in pixel_matrix needs to have the same number of columns
        #     - Every cell in pixel_matrix needs to be an RGB tuple or hex string
        """
        number_of_rows = len(pixel_matrix)
        number_of_columns = len(pixel_matrix[0])

        max_pixel_height = self.surface.get_height() // number_of_rows
        max_pixel_width = self.surface.get_width() // number_of_columns

        px_side_len = min(max_pixel_height, max_pixel_width)

        for row in range(0, number_of_rows):
            for col in range(0, number_of_columns):
                self.surface.fill(
                    pixel_matrix[row][col],
                    (col * px_side_len, row * px_side_len, px_side_len, px_side_len)
                )


class PixelMatrix:
    def __init__(self, width, height, fill_color="#000000"):
        self.matrix = [
            [fill_color for col in range(0, width)]
            for row in range(0, height)
        ]

    def get_width(self):
        return len(self.matrix[0])

    def get_height(self):
        return len(self.matrix)

    def set_pixel_color(self, point, color="#ffffff"):
        if point.x < 0 or point.y < 0:
            return

        try:
            self.matrix[point.y][point.x] = color
        except IndexError:
            pass

    def get_pixel_color(self, point):
        if point.x < 0 or point.y < 0:
            return None

        try:
            return self.matrix[point.y][point.x]
        except IndexError:
            return None
