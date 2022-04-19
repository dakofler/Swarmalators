import random as rnd
import math
from PIL import Image, ImageTk
import colorsys


class Swarmalator:
    def __init__(self, id, screen_size, phase=None):

        self.id = 'swrmltr' + str(id)

        self.x = rnd.randrange(10, screen_size - 10)
        self.y = rnd.randrange(10, screen_size - 10)

        self.angle = rnd.uniform(0.0, 2.0 * math.pi)
        self.speed = 0

        self.phase = phase if phase is not None else rnd.uniform(0.0, 2.0 * math.pi)
        self.d_phase = 0

        self.swarm_phases = {}
        self.swarm_positions = {}

       
    def draw_swarmalator(self, canvas):
        size = 10
        x1 = self.x + size
        x2 = self.y + size

        # color based on swarmalator phase
        c_val = self.phase / (2.0 * math.pi) % (2.0 * math.pi)
        c_rgb = colorsys.hsv_to_rgb(c_val, 1, 1)
        c_int = tuple(int(t * 255) for t in c_rgb)
        c_hex = '#%02x%02x%02x' % c_int

        canvas.create_oval(self.x, self.y, x1, x2, fill=c_hex, tags=self.id)

    def update(self, canvas, screen_size, delta_t):
        # update position
        distance = self.speed * delta_t

        # calculate next position the swarmalator moves to
        self.x += distance * math.cos(self.angle)
        self.y += distance * math.sin(self.angle)

        # when swarmalator goes off screen, will come back from other side of screen
        self.x = self.x % screen_size
        self.y = self.y % screen_size

        # update phase
        self.phase += self.d_phase * delta_t

        canvas.delete(self.id)
        self.draw_swarmalator(canvas)

    def euclidean_distance(self, neighbour_boid):
        return math.sqrt((self.x - neighbour_boid.x) * (self.x - neighbour_boid.x) + (self.y - neighbour_boid.y) * (self.y - neighbour_boid.y))