import random as rnd
import math
from PIL import Image, ImageTk
import colorsys
import numpy as np


class Swarmalator:
    def __init__(self, id, phase=None):

        self.id = 'swrmltr' + str(id)

        self.position = np.array([rnd.random() * 2 - 1, rnd.random() * 2 - 1])
        self.velocity = np.array([0, 0])

        self.phase = phase if phase is not None else rnd.uniform(0.0, 2.0 * math.pi)
        self.d_phase = 0

        self.neighbour_phases = {}
        self.neighbour_positions = {}

       
    def draw_swarmalator(self, canvas, screen_size):
        size = 10

        # color based on swarmalator phase
        c_val = self.phase / (2.0 * math.pi) % (2.0 * math.pi)
        c_rgb = colorsys.hsv_to_rgb(c_val, 1, 1)
        c_int = tuple(int(t * 255) for t in c_rgb)
        c_hex = '#%02x%02x%02x' % c_int

        canv_pos_x = self.position[0] * screen_size / 4 + screen_size / 2
        canv_pos_y = self.position[1] * screen_size / 4 + screen_size / 2

        x1 = canv_pos_x + size
        x2 = canv_pos_y + size

        canvas.create_oval(canv_pos_x, canv_pos_y, x1, x2, fill=c_hex, tags=self.id)

    def move(self, canvas, screen_size, delta_t):
        # calculate next position the swarmalator moves to
        self.position = self.position + self.velocity * delta_t

        # when swarmalator goes off screen, will come back from other side of screen
        if self.position[0] < -2.0: self.position[0] += 4.0
        if self.position[0] > 2.0: self.position[0] -= 4.0
        if self.position[1] < -2.0: self.position[1] += 4.0
        if self.position[1] > 2.0: self.position[1] -= 4.0

        # update phase
        self.phase = (self.phase + self.d_phase * delta_t) % (2.0 * math.pi)

        canvas.delete(self.id)
        self.draw_swarmalator(canvas, screen_size)