import random as rnd
import math
from PIL import Image, ImageTk


class Swarmalator:
    def __init__(self, label, phase=None):
        self.x = rnd.randrange(100, 900)
        self.y = rnd.randrange(100, 900)
        self.angle = rnd.uniform(0.0, 2.0 * math.pi)
        self.label = label
        self.color = "black"
        self.phase = phase if phase is not None else rnd.uniform(0.0, 2.0 * math.pi)

    def draw_swarmalator(self, canvas):
        size = 18
        x1 = self.x + size * math.cos(self.angle)
        x2 = self.y + size * math.sin(self.angle)
        canvas.create_line(self.x, self.y, x1, x2, fill='black', arrow='last', arrowshape=(12.8,16,4.8), width=2, tags=self.label)

    def step(self, canvas, screen_size):
        distance = 3

        # calculate next position the swarmalator moves to
        self.x += distance * math.cos(self.angle)
        self.y += distance * math.sin(self.angle)

        # when drone goes off screen, will come back from other side of screen
        self.x = self.x % screen_size
        self.y = self.y % screen_size
        canvas.delete(self.label)
        self.draw_swarmalator(canvas)

    def euclidean_distance(self, neighbour_boid):
        return math.sqrt((self.x - neighbour_boid.x) * (self.x - neighbour_boid.x) + (self.y - neighbour_boid.y) * (self.y - neighbour_boid.y))