import time
import math
import numpy as np
import tkinter as tk

from swarmalator_model.swarmalator import Swarmalator
from swarmalator_model.dataset import Dataset
from swarmalator_model import helper_functions as hlp


class Simulation:
    def __init__(self, plot_size: int ='1000', logging: bool=False,
        num_swarmalators: int=100,
        memory_init: str='random',
        time_step: float=0.1,
        coupling_probability: float=0.1,
        J: float=0.1,
        K: float=1.0,
        plot_type: str='positions',
        alpha: float=0,
        max_simulation_time: float=0):
        '''
        Instantiates the environment for a swarmalator-simulation.

        Parameters
        ----------
        plot_size : int, optional
            Size of the tkinter canvas. default=`1000`
        Logging : bool, optional
            Logs positions and velocities for later analysis. default=`False`
        num_swarmalators : int, optional
            Number of swarmalators in the simulation. default=`100`
        memory_init : {'random', 'zeroes', 'gradual'}, optional
            Method of swarmalator memory initialization. default=`random`
            `random`: random positions and phases.
            `zeroes`: initialize positions and phases as 0.
            `gradual`: initialize empty memory and learn positions and phases gradually.
        delta_t : float, optional
            Time step of an iteration in seconds. default=`0.1`
        coupling_probability : float, optional
            Probability that a swarmalator successfully receives information about another swarmalators position and phase per iteration. default=`0.1`
        J : float, optional
            Phase attraction strength. For J > 0 swarmalators with similar phases attract each other. For J < 0 opposite phased swarmalators are attracted. default=`0.1`
        K : float, optional
            Phase coupling strength. For K > 0 swarmalators try to minimize their phase difference. For K < 0 the difference is maximized. default=`1.0`
        plot_type : {'positions', 'phases'}, optional
            Type of data to be displayed. default=`positions`
        alpha : float, optional
            Momentum factor. Must be between 0 and 1. default=`0`
        max_simulation_time : float, optional
            Time in s after which the simulation is stopped automatically. The simulation does not stop, if it is `0`. default=`0`
        '''
        self.plot_size = plot_size
        self.logging = logging
        self.alpha = alpha
        self.max_simulation_time = max_simulation_time

        self.memory_log = []
        self.velocity_log = []
        self.list_of_swarmalators = []

        self.iteration = 1
        self.simulaton_time = 0
        self.comp_time = 0
        self.global_phase = 0
        self.paused = False
        self.stopped = True

        self.__init_canvas(num_swarmalators, memory_init, time_step, coupling_probability, J, K, plot_type)

    #region Core functions
    def run_simulation(self):
        '''
        Starts the main loop.
        '''
        self.__draw_coordinate_system()
        self.sim.mainloop()

    def __step(self):
        '''
        Makes each swarmalator perform one step of syncing and moving.
        '''
        if self.simulaton_time <= self.max_simulation_time or self.max_simulation_time == 0.0:
            wait_time = int(self.time_step * 1000.0)
            self.simulation_type = str(self.var_plot_type.get()) # read simulation type input to make live-switching possible

            if not self.stopped:
                if not self.paused:
                    start = time.time()

                    # update swarmalators
                    for s in self.list_of_swarmalators: s.run(self.memory, self.velocities, self.time_step, self.J, self.K, self.coupling_probability, self.alpha)
                    self.__draw_swarmalators()

                    # log time
                    end = time.time()
                    self.comp_time = int((end - start) * 1000)
                    dt = int(self.time_step * 1000)
                    wait_time = int(max(dt - self.comp_time, 1))
                    self.simulaton_time += self.time_step

                    # write data to labels
                    self.__update_labels()

                    # logging
                    if self.logging: self.__log()

                    self.iteration += 1
                    self.__tick(frequency=0.5)

                self.canvas.after(wait_time, self.__step)
        else:
            self.__stop_simulation()

    #endregion

    #region Other
    def __log(self):
        '''
        Stores the current memory and velocity to seperate lists each iteration for later analysis.
        '''
        self.memory_log.append(self.memory.copy())
        self.velocity_log.append(self.velocities.copy())
    
    def __tick(self, frequency):
        '''
        Updates the simulation clock.
        '''
        p = self.global_phase + (2 * math.pi * self.time_step * frequency)
        if p > math.pi: p -= 2 * math.pi
        if p < -math.pi: p += 2 * math.pi
        self.global_phase = p

    #endregion

    #region Initialization
    def __init_canvas(self, num_swarmalators: int, memory_init: str, time_step: float, coupling_probability: float, J: float, K: float, plot_type: str):
        '''
        Initializes the environment canvas object and all control elements.

        Parameters
        ----------
        num_swarmalators : int, optional
            Number of swarmalators in the simulation.
        memory_init : {'random', 'zeroes', 'gradual'}
            Method of swarmalator memory initialization.
            `random`: random positions and phases.
            `zeroes`: initialize positions and phases as 0.
            `gradual`: initialize empty memory and learn positions and phases gradually.
        time_step : float
            Time step of an iteration in seconds.
        coupling_probability : float
            Probability that a swarmalator successfully receives information about another swarmalators position and phase per iteration.
        J : float
            Phase attraction strength. For J > 0 swarmalators with similar phases attract each other. For J < 0 opposite phased swarmalators are attracted.
        K : float
            Phase coupling strength. For K > 0 swarmalators try to minimize their phase difference. For K < 0 the difference is maximized.
        plot_type : {'positions', 'phases'}, optional
            Type of data to be displayed.
        '''
        self.sim = tk.Tk()
        
        # Canvas
        self.canvas = tk.Canvas(self.sim, width=self.plot_size, height=self.plot_size)
        self.canvas.grid(row=0, column=0, rowspan=15)

        # Entry Number of Swarmalators
        tk.Label(self.sim, text='Number of swarmalators').grid(row=0, column=1, sticky='w')
        self.entry_num_swarmalators = tk.Entry(self.sim)
        self.entry_num_swarmalators.insert(0, str(num_swarmalators))
        self.entry_num_swarmalators.grid(row=0, column=2)

        # Entry Memory Init Method
        tk.Label(self.sim, text='Memory initialization').grid(row=1, column=1, sticky='w')
        self.var_memory_init = tk.StringVar(self.sim, memory_init)
        tk.Radiobutton(self.sim, text='random', variable=self.var_memory_init, value='random').grid(row=1, column=2)
        tk.Radiobutton(self.sim, text='zeroes', variable=self.var_memory_init, value='zeroes').grid(row=1, column=3)
        tk.Radiobutton(self.sim, text='gradual', variable=self.var_memory_init, value='gradual').grid(row=1, column=4)

        # Entry Time Step
        tk.Label(self.sim, text='Time step in s').grid(row=2, column=1, sticky='w')
        self.entry_time_step = tk.Entry(self.sim)
        self.entry_time_step.insert(0, str(time_step))
        self.entry_time_step.grid(row=2, column=2)

        # Entry Coupling Probabiltity
        tk.Label(self.sim, text='Coupling probability').grid(row=3, column=1, sticky='w')
        self.entry_coupling_probability = tk.Entry(self.sim)
        self.entry_coupling_probability.insert(0, str(coupling_probability))
        self.entry_coupling_probability.grid(row=3, column=2)

        # Entry J
        tk.Label(self.sim, text='J').grid(row=4, column=1, sticky='w')
        self.entry_J = tk.Entry(self.sim)
        self.entry_J.insert(0, str(J))
        self.entry_J.grid(row=4, column=2)

        # Entry K
        tk.Label(self.sim, text='K').grid(row=5, column=1, sticky='w')
        self.entry_K = tk.Entry(self.sim)
        self.entry_K.insert(0, str(K))
        self.entry_K.grid(row=5, column=2)

        # Entry Plot Type
        tk.Label(self.sim, text='Plot type').grid(row=6, column=1, sticky='w')
        self.var_plot_type = tk.StringVar(self.sim, plot_type)
        tk.Radiobutton(self.sim, text='positions', variable=self.var_plot_type, value='positions', command=self.__draw_coordinate_system).grid(row=6, column=2)
        tk.Radiobutton(self.sim, text='phases', variable=self.var_plot_type, value='phases', command=self.__draw_coordinate_system).grid(row=6, column=3)

        # Button Start
        self.btn_start = tk.Button(self.sim, text='Start/Reset simulation', command=self.__start_simulation)
        self.btn_start.grid(row=8, column=1)

        # Button Stop
        self.btn_stop = tk.Button(self.sim, text='Stop simulation', command=self.__stop_simulation)
        self.btn_stop.grid(row=8, column=2)
        self.btn_stop.config(state='disabled')

        # Button Pause
        self.btn_pause = tk.Button(self.sim, text='Pause simulation', command=self.__pause_simulation)
        self.btn_pause.grid(row=9, column=1)

        # Button Save Data
        tk.Button(self.sim, text='Save data', command=self.__save_data).grid(row=10, column=1)

        # Label Iteration
        self.lbl_iteration = tk.Label(self.sim, text='iteration = 1')
        self.lbl_iteration.grid(row=11, column=1, sticky='w')

        # Label Simulation Time
        self.lbl_sim_time = tk.Label(self.sim, text='sim_time = 0 s')
        self.lbl_sim_time.grid(row=12, column=1, sticky='w')

        # Label Computation Time
        self.lbl_comp_time = tk.Label(self.sim, text='comp_time = 0 s')
        self.lbl_comp_time.grid(row=13, column=1, sticky='w')

        self.sim.title('Swarmalators')
        self.sim.resizable(False, False)

    def __init_positions_phases(self):
        '''
        Initializes the environment memory with swarmalator positons, phases and velocities.
        '''
        self.memory = np.zeros((self.num_swarmalators, 3))
        self.velocities = np.zeros((self.num_swarmalators, 2))

        for i, s in enumerate(self.list_of_swarmalators):
            self.memory[i] = s.memory[i]
            self.velocities[i] = s.velocity

    def __init_swarmalators(self):
        '''
        Adds new swarmalator objects to the envionment.
        '''
        self.list_of_swarmalators.clear()
        for n in range(self.num_swarmalators):
            s = Swarmalator(n, self.num_swarmalators, self.memory_init)
            self.list_of_swarmalators.append(s)

    #endregion

    #region Updating
    def __read_inputs(self):
        '''
        Reads values from the input control elements.
        '''
        try:
            self.num_swarmalators = int(self.entry_num_swarmalators.get())
            self.memory_init = str(self.var_memory_init.get())
            self.time_step = round(float(self.entry_time_step.get()), 2)
            self.coupling_probability = round(float(self.entry_coupling_probability.get()), 2)
            self.J = round(float(self.entry_J.get()), 2)
            self.K = round(float(self.entry_K.get()), 2)
            self.simulation_type = str(self.var_plot_type.get())
            return True
        except:
            print('Error reading inputs.')
            return False

    def __update_labels(self):
        self.lbl_iteration['text'] = f'iteration = {self.iteration}'
        self.lbl_sim_time['text'] = f'sim_time = {round(self.simulaton_time, 1)} s'
        self.lbl_comp_time['text'] = f'step_comp_time = {round(self.comp_time, 0)} ms'

    #endregion

    #region Button Events
    def __start_simulation(self):
        '''
        Starts a simulation run.
        '''
        if not self.__read_inputs(): return
        self.paused = False
        self.stopped = False
        self.iteration = 1
        self.simulaton_time = 0
        self.memory_log.clear()
        self.velocity_log.clear()
        self.btn_pause['text'] = 'Pause Simulation'
        self.btn_start.config(state='disabled')
        self.btn_stop.config(state='active')

        self.__draw_coordinate_system()
        self.canvas.update()
        self.__init_swarmalators()
        self.__init_positions_phases()
        self.__step()

    def __stop_simulation(self):
        '''
        Stops the active simulation run.
        '''
        self.stopped = True
        self.canvas.delete("s")
        self.btn_start.config(state='active')
        self.btn_stop.config(state='disabled')

    def __pause_simulation(self):
        '''
        Pauses the simulation if one is currently running. Otherwise resumes current simulation.
        '''
        if not self.stopped:
            self.paused = not self.paused
            if self.paused: self.btn_pause['text'] = 'Resume Simulation'
            else: self.btn_pause['text'] = 'Pause Simulation'
    
    def __save_data(self):
        '''
        Saves logged information to a Dataset object.
        '''
        parameters = {
            'dt' : self.time_step,
            'j' : self.J,
            'k' : self.K,
            'cp' : self.coupling_probability,
            'a' : self.alpha
        }
        
        data = [self.memory_log, self.velocity_log, round(self.simulaton_time, 2), parameters]
        Dataset(data).save_to_file()

    #endregion

    #region Drawing
    def __draw_coordinate_system(self):
        '''
        Draws a coordinate system on the canvas.
        '''
        areas = 8
        self.canvas.delete('all')
        self.simulation_type = str(self.var_plot_type.get())
        
        for i in range(1, areas):
            x_x0 = y_y0 = 0.0
            x_y0 = x_y1 = y_x0 = y_x1 = self.plot_size / areas * i
            x_x1 = y_y1 = self.plot_size

            if i == areas / 2.0:
                self.canvas.create_line(x_x0, x_y0, x_x1, x_y1, width=2) # main x axis
                self.canvas.create_line(y_x0, y_y0, y_x1, y_y1, width=2) # main y axis

                for j in range(1, areas):
                    if self.simulation_type == 'positions': t = j * 4.0 / areas - 2.0
                    else: t = round(j * 2.0 * math.pi / areas - math.pi, 2)
                    self.canvas.create_text(self.plot_size / areas * j + 15.0, self.plot_size / 2.0 + 15.0, text=str(t)) # x axis labels
                    if j != areas / 2.0: self.canvas.create_text(self.plot_size / 2.0 + 15.0, self.plot_size / areas * j + 15.0, text=str(-t)) # y axis labels
                
            else:
                self.canvas.create_line(x_x0, x_y0, x_x1, x_y1, dash=(2, 2)) # helper x axis
                self.canvas.create_line(y_x0, y_y0, y_x1, y_y1, dash=(2, 2)) # helper y axis

    def __draw_swarmalators(self):
        '''
        Draws swarmalators on the canvas.
        '''
        self.canvas.delete("s")
        if self.simulation_type == 'positions': self.__draw_positions()
        else: self.__draw_phases()

    def __draw_positions(self):
        '''
        Draws swarmalators on the canvas based on their position.
        '''
        size = self.plot_size / 120
        for i in range(self.num_swarmalators):
            p = self.global_phase + self.memory[i][2]
            if p > math.pi: p -= 2 * math.pi
            if p < -math.pi: p += 2 * math.pi
            color = hlp.phase_to_hex(p)

            x1 = self.plot_size * ((self.memory[i][0] + 2.0 ) / 4.0)
            y1 = (self.plot_size * ((-self.memory[i][1] + 2.0 ) / 4.0))

            diff_vec = self.velocities[i] / np.linalg.norm(self.velocities[i]) * size
            x2 = x1 + diff_vec[0]
            y2 = y1 - diff_vec[1]

            self.canvas.create_line(
                x1, y1, x2, y2, fill=color, tags='s',
                arrow=tk.LAST, arrowshape=(8 * size / 5, 10 * size / 5, 3 * size / 5))
            # self.canvas.create_text(x2, y2, text=str(i), tags='s')

    def __draw_phases(self):
        '''
        Draws swarmalators on the canvas based on their phase.
        '''
        size = self.plot_size / 150
        for i in range(self.num_swarmalators):
            a = math.atan(self.memory[i][1] / self.memory[i][0])
            if self.memory[i][0] < 0 and self.memory[i][1] > 0: a += math.pi
            elif self.memory[i][0] < 0 and self.memory[i][1] < 0: a -= math.pi

            x1 = self.plot_size * ((a / math.pi + 1.0 ) / 2.0)
            y1 = self.plot_size * ((-self.memory[i][2] / math.pi + 1.0 ) / 2.0)
            x2 = x1 + size
            y2 = y1 + size

            self.canvas.create_oval(x1, y1, x2, y2, fill='black', tags='s')
    
    #endregion