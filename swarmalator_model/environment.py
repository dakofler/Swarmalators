import random as rnd
import time
import math
import colorsys
import numpy as np
import tkinter as tk

from sqlalchemy import true
from swarmalator_model.swarmalator import Swarmalator

class Environment:
    def __init__(self, num_swarmalators, memory_init = 'rand', screen_size='1000'):
        self.num_swarmalators = num_swarmalators
        self.memory_init = memory_init
        self.screen_size = screen_size
        self.list_of_swarmalators = []

    def init_positions_phases(self):
        self.phases = np.zeros(self.num_swarmalators)
        self.positions = np.zeros((self.num_swarmalators, 2))      

        for i, s in enumerate(self.list_of_swarmalators):
            self.positions[i] = s.positions[i]
            self.phases[i] = s.phases[i]

    def init_canvas(self):
        self.canvas = tk.Canvas(self.sim, width=self.screen_size, height=self.screen_size)
        self.canvas.pack()
        self.sim.resizable(False, False)

    def add_swarmalators(self):
        self.list_of_swarmalators.clear()
        for n in range(self.num_swarmalators):
            s = Swarmalator(n, self.num_swarmalators, self.memory_init)
            self.list_of_swarmalators.append(s)

    def run(self, delta_t, J, K, coupling_probability=0.1):
        self.sim = tk.Tk()
        self.init_canvas()
        self.add_swarmalators()
        self.init_positions_phases()
        self.draw()

        self.iteration(delta_t, J, K, coupling_probability)
        self.sim.mainloop()

    def iteration(self, delta_t, J, K, coupling_probability):
        start = time.time()

        for s in self.list_of_swarmalators:
            
            s.run(self.list_of_swarmalators, self.positions, self.phases, delta_t, J, K, coupling_probability)

        self.draw()
        end = time.time()
        comp_time = end - start
        print(f'comp_time={round((end - start) * 1000, 2)}ms')
        self.canvas.after(max(int(delta_t * 1000 - comp_time), int(delta_t * 1000)), self.iteration, delta_t, J, K, coupling_probability)

    def draw(self):
        size = 10

        self.canvas.delete('all')

        for i in range(len(self.positions)):
            # color based on swarmalator phase
            c_val = self.phases[i] / (2.0 * math.pi) % (2.0 * math.pi)
            c_rgb = colorsys.hsv_to_rgb(c_val, 1, 1)
            c_int = tuple(int(t * 255) for t in c_rgb)
            c_hex = '#%02x%02x%02x' % c_int

            x1 = self.positions[i][0] * self.screen_size / 4 + self.screen_size / 2
            y1 = self.positions[i][1] * self.screen_size / 4 + self.screen_size / 2
            x2 = x1 + size
            y2 = y1 + size

            self.canvas.create_oval(x1, y1, x2, y2, fill=c_hex, tags='s' + str(i))  