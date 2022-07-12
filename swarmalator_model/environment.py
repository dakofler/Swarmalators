import time
import numpy as np
import tkinter as tk

from multiprocessing import Process
import threading

from swarmalator_model.swarmalator import Swarmalator
from swarmalator_model import functions as fct


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

        # processes = []
        # threads = []

        # for s in self.list_of_swarmalators:
            # process = Process(target=s.run, args=(self.list_of_swarmalators, self.positions, self.phases, delta_t, J, K, coupling_probability))
            # processes.append(process)

            # thread = threading.Thread(target=s.run, args=(self.list_of_swarmalators, self.positions, self.phases, delta_t, J, K, coupling_probability))
            # threads.append(thread)
        
        # for p in processes:
        #     p.start()

        # for t in threads:
        #     t.start()

        self.iteration(delta_t, J, K, coupling_probability)
        self.sim.mainloop()

    def iteration(self, delta_t, J, K, coupling_probability):
        start = time.time()

        for s in self.list_of_swarmalators:
            s.run(self.positions, self.phases, delta_t, J, K, coupling_probability)

        self.draw()
        end = time.time()
        print(f'step={round((end - start) * 1000)}ms')

        wait_time = max(int(delta_t * 1000 - (end - start)), 1)
        self.canvas.after(wait_time, self.iteration, delta_t, J, K, coupling_probability)

    def draw(self):
        size = 10
        self.canvas.delete('all')

        for i in range(self.num_swarmalators):
            color = fct.phase_to_hex(self.phases[i])

            x1 = self.screen_size * (self.positions[i][0] + 2.0) / 4.0
            y1 = self.screen_size * (self.positions[i][1] + 2.0) / 4.0
            x2 = x1 + size
            y2 = y1 + size

            self.canvas.create_oval(x1, y1, x2, y2, fill=color, tags='s' + str(i))  