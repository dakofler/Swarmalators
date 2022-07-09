import random as rnd
import math
import colorsys
import numpy as np
import tkinter as tk


class Swarmalator:
    def __init__(self, id, num_of_swarmalators, memory_init):
        '''Creates a swarmalator instance.

        Parameters
        ----------
            id (int): id of the swarmalator.
            num_of_swarmalators (int): number of swarmalators used in the model
            memory_init (string): Determines how position and phase memories of swarmalators are initialized. Options: `zero`, `rand`
        '''
        self.id = id

        self.velocity = np.zeros(2)
        self.d_phase = 0

        # initialize memories with random values
        if memory_init == 'rand':
            self.phases = np.random.rand(num_of_swarmalators) * 2 * math.pi #phase-vector
            self.positions = np.random.rand(num_of_swarmalators, 2) * 2 - 1 #position-array
        else:
            self.phases = np.zeros(num_of_swarmalators) #phase-vector
            self.positions = np.zeros((num_of_swarmalators, 2)) #position-vector

            # initialize own position and phase randomly
            self.positions[self.id][0] = rnd.random() * 2 - 1
            self.positions[self.id][1] = rnd.random() * 2 - 1
            self.phases[self.id] = rnd.uniform(0.0, 2.0 * math.pi)           
       
    def draw_swarmalator(self, canvas, screen_size):
        '''Adds the swarmalator to a canvas instance.

        Parameters
        ----------
            canvas (tikinter.Canvas): Canvas object the swarmalators should be added to.
            screen_size (int): size of the canvas
        '''
        size = 1.75

        # color based on swarmalator phase
        c_val = self.phases[self.id] / (2.0 * math.pi) % (2.0 * math.pi)
        c_rgb = colorsys.hsv_to_rgb(c_val, 1, 1)
        c_int = tuple(int(t * 255) for t in c_rgb)
        c_hex = '#%02x%02x%02x' % c_int

        x1 = self.positions[self.id][0] * screen_size / 4 + screen_size / 2
        y1 = self.positions[self.id][1] * screen_size / 4 + screen_size / 2
        diff_vec = self.velocity / np.linalg.norm(self.velocity) * size * 5
        x2 = x1 + diff_vec[0]
        y2 = y1 + diff_vec[1]

        # canvas.create_oval(canv_pos_x, canv_pos_y, x1, x2, fill=c_hex, tags='s' + str(self.id))
        canvas.create_line(x2, y2, x1, y1, fill=c_hex, tags='s' + str(self.id), arrow=tk.FIRST, arrowshape=(8 * size, 10 * size, 3 * size))


    def step(self, list_of_swarmalators, delta_t, J, K, coupling_probability):
        '''Makes the swarmalator sync, update and move.

        Parameters
        ----------
            list_of_swarmalators (list[swarmalator_model.Swarmalator]): List of swarmalator objects
            delta_t (float): value of one euler step
            J (float): Parameter that influences the attraction and repulsion between swarmalators
            K (float): Parameter that influences the phase synchronization between swarmalators
            coupling_probability (float): Probability for a swarmalator to update its information about neighbours
        '''
        self.synchronize(list_of_swarmalators, coupling_probability)
        self.update(len(list_of_swarmalators), J, K)
        self.move(delta_t)

    def move(self, delta_t):
        '''Computes the swarmalators new position.

        Parameters
        ----------
            delta_t (float): value of one euler step

        '''
        # calculate next position the swarmalator moves to
        self.positions[self.id] = self.positions[self.id] + self.velocity * delta_t

        # update phase
        self.phases[self.id] = (self.phases[self.id] + self.d_phase * delta_t) % (2.0 * math.pi)
    
    def update(self, num_of_swarmalators, J, K):
        '''Updates the position and phase of a swarmalator based on it's neighbours.

        Parameters
        ----------
            num_of_swarmalators (int): number of swarmalators used in the model
            J (float): Parameter that influences the attraction and repulsion between swarmalators
            K (float): Parameter that influences the phase synchronization between swarmalators
        '''
        v_temp = np.zeros(2)
        p_temp = 0.0

        for i in range(num_of_swarmalators):
            if i != self.id:
                d_x = self.positions[i] - self.positions[self.id]
                d_theta = self.phases[i] - self.phases[self.id]
                d_x_norm = np.linalg.norm(d_x)
                
                v_temp += (d_x / d_x_norm * (1.0 + J * math.cos(d_theta)) - d_x / (d_x_norm * d_x_norm))
                p_temp += math.sin(d_theta) / d_x_norm

        self.velocity = 1 / (len(self.positions)) * v_temp
        self.d_phase = K / (len(self.phases)) * p_temp

    def synchronize(self, list_of_swarmalators, coupling_probability):
        '''Updates a swarmalator's memory of positions and phases of it's neighbours.

        Parameters
        ----------
            list_of_swarmalators (list[swarmalator_model.Swarmalator]): List of swarmalator objects
            coupling_probability (float): Probability for a swarmalator to update its information about neighbours
        '''
        for i in range(len(self.positions)):
            if i != self.id:
                r = rnd.random()
                if r <= coupling_probability:
                    self.positions[i] = list_of_swarmalators[i].positions[i]
                    self.phases[i] = list_of_swarmalators[i].phases[i]