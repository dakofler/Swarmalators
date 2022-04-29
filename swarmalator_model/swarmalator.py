import random as rnd
import math
import colorsys
import numpy as np


class Swarmalator:
    def __init__(self, id, phase=None):
        '''Creates a swarmalator instance.

        Parameters
        ----------
            id (str): id of the swarmalator.
            phase (float): pahse of the swarmalator (default `None`)
        '''
        self.id = 'swrmltr' + str(id)
        self.position = np.array([rnd.random() * 2 - 1, rnd.random() * 2 - 1])
        self.velocity = np.array([0, 0])
        self.phase = phase if phase is not None else rnd.uniform(0.0, 2.0 * math.pi)
        self.d_phase = 0
        self.neighbour_phases = {}
        self.neighbour_positions = {}
       
    def draw_swarmalator(self, canvas, screen_size):
        '''Adds the swarmalator to a canvas instance.

        Parameters
        ----------
            canvas (tikinter.Canvas): Canvas object the swarmalators should be added to.
            screen_size (int): size of the canvas
        '''
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

    def step(self, list_of_swarmalators, canvas, screen_size, delta_t, J, K, coupling_probability):
        '''Makes the swarmalator sync, update and move.

        Parameters
        ----------
            list_of_swarmalators (list[swarmalator_model.Swarmalator]): List of swarmalator objects
            canvas (tikinter.Canvas): Canvas object the swarmalators should be added to.
            screen_size (int): size of the canvas
            delta_t (float): value of one euler step
            J (float): Parameter that influences the attraction and repulsion between swarmalators
            K (float): Parameter that influences the phase synchronization between swarmalators
            coupling_probability (float): Probability for a swarmalator to update its information about neighbours
        '''
        self.synchronize(list_of_swarmalators, coupling_probability)
        self.update(list_of_swarmalators, J, K)
        self.move(canvas, screen_size, delta_t)

    def move(self, delta_t):
        '''Computes the swarmalators new position.

        Parameters
        ----------
            delta_t (float): value of one euler step

        '''
        # calculate next position the swarmalator moves to
        self.position = self.position + self.velocity * delta_t

        # when swarmalator goes off screen, will come back from other side of screen
        if self.position[0] < -2.0: self.position[0] += 4.0
        if self.position[0] > 2.0: self.position[0] -= 4.0
        if self.position[1] < -2.0: self.position[1] += 4.0
        if self.position[1] > 2.0: self.position[1] -= 4.0

        # update phase
        self.phase = (self.phase + self.d_phase * delta_t) % (2.0 * math.pi)
    
    def update(self, list_of_swarmalators, J, K):
        '''Updates the position and pahse of a swarmalator based on it's neighbours.

        Parameters
        ----------
            list_of_swarmalators (list[swarmalator_model.Swarmalator]): List of swarmalator objects
            J (float): Parameter that influences the attraction and repulsion between swarmalators
            K (float): Parameter that influences the phase synchronization between swarmalators
        '''
        if self.neighbour_positions and self.neighbour_phases:
            x_i = self.position
            theta_i = self.phase

            v_temp = np.array([0.0, 0.0])
            p_temp = 0.0

            for swarmalator_j in list_of_swarmalators:
                if swarmalator_j.id != self.id and swarmalator_j.id in self.neighbour_positions and swarmalator_j.id in self.neighbour_phases:
                    x_j = self.neighbour_positions[swarmalator_j.id]
                    theta_j = self.neighbour_phases[swarmalator_j.id]
                    
                    d_x = x_j - x_i
                    d_theta = theta_j - theta_i
                    d_x_norm = np.linalg.norm(d_x)
                    
                    v_temp += (d_x / d_x_norm * (1.0 + J * math.cos(d_theta)) - d_x / (d_x_norm * d_x_norm))
                    p_temp += math.sin(d_theta) / d_x_norm

            self.velocity = 1 / (len(self.neighbour_positions)) * v_temp
            self.d_phase = K / (len(self.neighbour_phases)) * p_temp

    def synchronize(self, list_of_swarmalators, coupling_probability):
        '''Updates a swarmalator's memory of positions and phases of it's neighbours.

        Parameters
        ----------
            list_of_swarmalators (list[swarmalator_model.Swarmalator]): List of swarmalator objects
            coupling_probability (float): Probability for a swarmalator to update its information about neighbours
        '''
        for s in list_of_swarmalators:
            if s.id != self.id:
                r = rnd.random()
                if r <= coupling_probability:
                    self.neighbour_positions[s.id] = s.position
                    self.neighbour_phases[s.id] = s.phase