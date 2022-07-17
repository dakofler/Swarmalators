import time
import numpy as np
import tkinter as tk
from swarmalator_model.swarmalator import Swarmalator
from swarmalator_model import functions as fct


class Environment:
    def __init__(self, num_swarmalators: int, memory_init: str = 'random', screen_size: int ='1000'):
        '''
        Instantiates the environment for a swarmalator-simulation.

        Parameters
        ----------
        num_swarmalators : int
            Number of swarmalators to be simulated.
        memory_init : {'random', 'zeroes'}, optional
            Method of swarmalator memory initialization. `rand` (random positions and phases) `zero` (initialize positions and phases as 0)
        screen_size : int, optional
            Window size of the tkinter canvas. default=`1000`
        '''
        self.num_swarmalators = num_swarmalators
        self.memory_init = memory_init if memory_init in ['random', 'zeroes'] else 'random'
        self.screen_size = screen_size
        self.list_of_swarmalators = []

    def init_positions_phases(self):
        '''
        Initializes the environment memory with swarmalator positons, phases and velocities.
        '''
        self.memory = np.zeros((self.num_swarmalators, 3))
        self.velocities = np.zeros((self.num_swarmalators, 2))

        for i, s in enumerate(self.list_of_swarmalators):
            self.memory[i] = s.memory[i]
            self.velocities[i] = s.velocity

    def init_canvas(self):
        '''
        Initializes the environment canvas object.
        '''
        self.canvas = tk.Canvas(self.sim, width=self.screen_size, height=self.screen_size)
        self.canvas.pack()
        self.sim.resizable(False, False)

    def add_swarmalators(self):
        '''
        Adds new swarmalator objects to the envionment.
        '''
        self.list_of_swarmalators.clear()
        for n in range(self.num_swarmalators):
            s = Swarmalator(n, self.num_swarmalators, self.memory_init)
            self.list_of_swarmalators.append(s)

    def run(self, delta_t: float, J: float, K: float, coupling_probability: float = 0.1):
        '''
        Starts a swarmalator-simulation.

        Parameters
        ----------
        delta_t : float
            Time step of an iteration.
        J : float
            Phase attraction strength. For J>0 swarmalators with similar phases attract each other. For J<0 opposite phased swarmalators are attracted.
        K : float
            Phase coupling strength. For K>0 swarmalators try to minimize their phase difference. For K<0 the difference is maximized.
        coupling_probability : float, optional
            Probability that a swarmalator successfully receives information about another swarmalators position and phase. default=`0.1`
        '''
        self.sim = tk.Tk()
        self.init_canvas()
        self.add_swarmalators()
        self.init_positions_phases()
        self.draw()

        self.iteration(delta_t, J, K, coupling_probability)
        self.sim.mainloop()

    def iteration(self, delta_t: float, J: float, K: float, coupling_probability: float):
        '''
        Makes each swarmalator perform an interation of syncing and moving.

        Parameters
        ----------
        delta_t : float
            Time step of an iteration.
        J : float
            Phase attraction strength. For J>0 swarmalators with similar phases attract each other. For J<0 opposite phased swarmalators are attracted.
        K : float
            Phase coupling strength. For K>0 swarmalators try to minimize their phase difference. For K<0 the difference is maximized.
        coupling_probability : float
            Probability that a swarmalator successfully receives information about another swarmalators position and phase.
        '''
        start = time.time()

        for s in self.list_of_swarmalators:
            s.run(self.memory, self.velocities, delta_t, J, K, coupling_probability)
        self.draw()

        end = time.time()
        comp_time = int((end - start) * 1000)
        dt = int(delta_t * 1000)
        wait_time = int(max(dt - comp_time, 1))
        print(f'comp_time={comp_time}ms, step={wait_time + comp_time}ms')

        self.canvas.after(wait_time, self.iteration, delta_t, J, K, coupling_probability)

    def draw(self):
        '''
        Draws swarmalators on the canvas.
        '''
        size = 10
        self.canvas.delete('all')

        for i in range(self.num_swarmalators):
            color = fct.phase_to_hex(self.memory[i][2])

            x1 = self.screen_size * (self.memory[i][0] + 2.0) / 4.0
            y1 = self.screen_size * (self.memory[i][1] + 2.0) / 4.0

            diff_vec = self.velocities[i] / np.linalg.norm(self.velocities[i]) * size
            x2 = x1 + diff_vec[0]
            y2 = y1 + diff_vec[1]

            self.canvas.create_line(
                x2, y2, x1, y1, fill=color, tags='s' + str(i),
                arrow=tk.FIRST, arrowshape=(8 * size / 5, 10 * size / 5, 3 * size / 5))