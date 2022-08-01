import time
import numpy as np
import tkinter as tk
import math
import pandas as pd
from swarmalator_model.swarmalator import Swarmalator
from swarmalator_model import functions as fct


class Environment:
    def __init__(self, num_swarmalators: int, memory_init: str = 'random', plot_size: int ='1000'):
        '''
        Instantiates the environment for a swarmalator-simulation.

        Parameters
        ----------
        num_swarmalators : int
            Number of swarmalators to be simulated.
        memory_init : {'random', 'zeroes'}, optional
            Method of swarmalator memory initialization. `rand` (random positions and phases) `zero` (initialize positions and phases as 0)
        plot_size : int, optional
            Size of the tkinter canvas. default=`1000`
        '''
        self.num_swarmalators = num_swarmalators
        self.plot_size = plot_size

        if memory_init in ['zeroes', 'random', 'gradual']: self.memory_init = memory_init
        else:
            self.memory_init = 'random'
            print('Unknown memory init method.\nMust be "zeroes", "random" or "gradual".\nMethod was set to "random"')

        self.list_of_swarmalators = []
        self.iteration = 1
        self.simulaton_time = 0
        self.paused = False

    def init_positions_phases(self):
        '''
        Initializes the environment memory with swarmalator positons, phases and velocities.
        '''
        self.memory = np.zeros((self.num_swarmalators, 3))
        self.velocities = np.zeros((self.num_swarmalators, 2))

        for i, s in enumerate(self.list_of_swarmalators):
            self.memory[i] = s.memory[i]
            self.velocities[i] = s.velocity

    def init_canvas(self, sim_mode):
        '''
        Initializes the environment canvas object.
        '''       
        self.sim = tk.Tk()
        
        self.lbl_plot_title = tk.Label(self.sim, text=f'Swarmalator {sim_mode}', font=("Arial", 14))
        self.lbl_plot_title.grid(row=0, column=0, columnspan=3)
        
        self.canvas = tk.Canvas(self.sim, width=self.plot_size, height=self.plot_size)
        self.canvas.grid(row=1, columnspan=3)

        self.btn_pause = tk.Button(self.sim, text='Pause Simulation', command=self.pause_simulation)
        self.btn_pause.grid(row=2, column=1)

        self.btn_show_data = tk.Button(self.sim, text='Show data', command=self.show_data)
        self.btn_show_data.grid(row=2, column=2)

        self.lbl_iteration = tk.Label(self.sim, text=f'iteration = {self.iteration}')
        self.lbl_iteration.grid(row=3, column=0)

        self.lbl_sim_time = tk.Label(self.sim, text=f'sim_time = {self.simulaton_time} s')
        self.lbl_sim_time.grid(row=3, column=1)

        self.lbl_comp_time = tk.Label(self.sim, text=f'comp_time = 0 s')
        self.lbl_comp_time.grid(row=3, column=2)

        self.sim.title('Swarmalators')
        self.sim.resizable(False, False)

    def pause_simulation(self):
        '''
        Pauses the simulation.
        '''
        self.paused = not self.paused
        if self.paused: self.btn_pause['text'] = 'Resume Simulation'
        else: self.btn_pause['text'] = 'Pause Simulation'

    def show_data(self):
        '''
        Shows positions and velocities of each swarmalator.
        '''
        print(pd.DataFrame(self.memory))

    def add_swarmalators(self):
        '''
        Adds new swarmalator objects to the envionment.
        '''
        self.list_of_swarmalators.clear()
        for n in range(self.num_swarmalators):
            s = Swarmalator(n, self.num_swarmalators, self.memory_init)
            self.list_of_swarmalators.append(s)

    def run_simulation(self, sim_mode: str, delta_t: float, J: float, K: float, coupling_probability: float = 0.1):
        '''
        Starts a swarmalator-simulation.

        Parameters
        ----------
        sim_mode : string
            Type of simulation, can be `positions` or `phases`
        delta_t : float
            Time step of an iteration.
        J : float
            Phase attraction strength. For J>0 swarmalators with similar phases attract each other. For J<0 opposite phased swarmalators are attracted.
        K : float
            Phase coupling strength. For K>0 swarmalators try to minimize their phase difference. For K<0 the difference is maximized.
        coupling_probability : float, optional
            Probability that a swarmalator successfully receives information about another swarmalators position and phase. default=`0.1`
        '''
        if sim_mode not in ['positions', 'phases']:
            print('Bad sim_mode. Must be "positions" or "phases".')
            return        

        self.paused = False
        self.iteration = 1
        self.simulaton_time = 0

        self.init_canvas(sim_mode)
        self.add_swarmalators()
        self.init_positions_phases()

        self.iterate(sim_mode, delta_t, J, K, coupling_probability)
        self.sim.mainloop()

    def iterate(self, sim_mode: str, delta_t: float, J: float, K: float, coupling_probability: float):
        '''
        Makes each swarmalator perform an interation of syncing and moving.

        Parameters
        ----------
        sim_mode : string
            Type of simulation, can be `positions` or `phases`
        delta_t : float
            Time step of an iteration.
        J : float
            Phase attraction strength. For J>0 swarmalators with similar phases attract each other. For J<0 opposite phased swarmalators are attracted.
        K : float
            Phase coupling strength. For K>0 swarmalators try to minimize their phase difference. For K<0 the difference is maximized.
        coupling_probability : float
            Probability that a swarmalator successfully receives information about another swarmalators position and phase.
        '''
        wait_time = int(delta_t * 1000)

        if not self.paused:
            start = time.time()

            # update swarmalators
            for s in self.list_of_swarmalators:
                s.run(self.memory, self.velocities, delta_t, J, K, coupling_probability)
            self.draw(sim_mode)

            # log time
            end = time.time()
            comp_time = int((end - start) * 1000)
            dt = int(delta_t * 1000)
            wait_time = int(max(dt - comp_time, 1))
            self.simulaton_time += delta_t

            # write data to labels
            self.lbl_iteration['text'] = f'iteration = {self.iteration}'
            self.lbl_sim_time['text'] = f'sim_time = {round(self.simulaton_time, 1)} s'
            self.lbl_comp_time['text'] = f'step_comp_time = {round(comp_time, 0)} ms'

            # ToDo: log positions, phases and potential calculated variables (change in velocity for convergence)

            self.iteration += 1

        self.canvas.after(wait_time, self.iterate, sim_mode, delta_t, J, K, coupling_probability)

    def draw(self, sim_mode: str):
        '''
        Draws swarmalators on the canvas.

        Parameters
        ----------
        sim_mode : string
            Type of simulation, can be `positions` or `phases`
        '''
        self.canvas.delete('all')
        self.draw_coordinate_system(sim_mode, 8)
        if sim_mode == 'positions': self.draw_positions()
        else: self.draw_phases()

    def draw_coordinate_system(self, sim_mode: str, areas: int):
        '''
        Draws a coordinate system on the canvas.

        Parameters
        ----------
        sim_mode : string
            Type of simulation. Can be `positions` or `phases`.
        areas : int
            Defines the helper line spacing.
        '''
        for i in range(1, areas):
            x_x0 = y_y0 = 0.0
            x_y0 = x_y1 = y_x0 = y_x1 = self.plot_size / areas * i
            x_x1 = y_y1 = self.plot_size

            if i == areas / 2.0:
                self.canvas.create_line(x_x0, x_y0, x_x1, x_y1, width=2) # main x axis
                self.canvas.create_line(y_x0, y_y0, y_x1, y_y1, width=2) # main y axis

                for j in range(1, areas):
                    if sim_mode == 'positions': t = j * 4.0 / areas - 2.0
                    else: t = round(j * 2.0 * math.pi / areas - math.pi, 2)
                    self.canvas.create_text(self.plot_size / areas * j + 15.0, self.plot_size / 2.0 + 15.0, text=str(t)) # x axis labels
                    if j != areas / 2.0: self.canvas.create_text(self.plot_size / 2.0 + 15.0, self.plot_size / areas * j + 15.0, text=str(-t)) # y axis labels
                
            else:
                self.canvas.create_line(x_x0, x_y0, x_x1, x_y1, dash=(2, 2)) # helper x axis
                self.canvas.create_line(y_x0, y_y0, y_x1, y_y1, dash=(2, 2)) # helper y axis

    def draw_positions(self):
        '''
        Draws swarmalators on the canvas based on their position.
        '''
        size = self.plot_size / 100
        for i in range(self.num_swarmalators):
            color = fct.phase_to_hex(self.memory[i][2])

            x1 = self.plot_size * ((self.memory[i][0] + 2.0 ) / 4.0)
            y1 = self.plot_size * ((self.memory[i][1] + 2.0 ) / 4.0)

            diff_vec = self.velocities[i] / np.linalg.norm(self.velocities[i]) * size
            x2 = x1 + diff_vec[0]
            y2 = y1 + diff_vec[1]

            self.canvas.create_line(
                x2, y2, x1, y1, fill=color, tags='s' + str(i),
                arrow=tk.FIRST, arrowshape=(8 * size / 5, 10 * size / 5, 3 * size / 5))

    def draw_phases(self):
        '''
        Draws swarmalators on the canvas based on their phase.
        '''
        size = self.plot_size / 100
        for i in range(self.num_swarmalators):
            a = math.atan(self.memory[i][1] / self.memory[i][0])
            if self.memory[i][0] < 0 and self.memory[i][1] > 0: a += math.pi
            elif self.memory[i][0] < 0 and self.memory[i][1] < 0: a -= math.pi

            x1 = self.plot_size * ((a / math.pi + 1.0 ) / 2.0)
            y1 = self.plot_size * ((self.memory[i][2] / math.pi + 1.0 ) / 2.0)
            x2 = x1 + size
            y2 = y1 + size

            self.canvas.create_oval(x2, y2, x1, y1, fill='black', tags='s' + str(i))