import random as rnd
import math
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

    def step(self, positions, phases, delta_t, J, K, coupling_probability):
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
        self.synchronize(positions, phases, coupling_probability)
        self.think(positions, phases, J, K)
        self.move(delta_t)

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
    
    def think(self, positions, phases, J, K):
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

            for p in positions:
                if self.id != p and p in phases:
                    x_j = positions[p]
                    theta_j = phases[p]
                    
                    d_x = x_j - x_i
                    d_theta = theta_j - theta_i
                    d_x_norm = np.linalg.norm(d_x)
                    
                    v_temp += (d_x / d_x_norm * (1.0 + J * math.cos(d_theta)) - d_x / (d_x_norm * d_x_norm))
                    p_temp += math.sin(d_theta) / d_x_norm

            self.velocity = 1 / (len(self.neighbour_positions)) * v_temp
            self.d_phase = K / (len(self.neighbour_phases)) * p_temp

    def synchronize(self, positions, phases, coupling_probability):
        '''Updates a swarmalator's memory of positions and phases of it's neighbours.

        Parameters
        ----------
            list_of_swarmalators (list[swarmalator_model.Swarmalator]): List of swarmalator objects
            coupling_probability (float): Probability for a swarmalator to update its information about neighbours
        '''
        r = rnd.random()
        for p in positions:
            if p != self.id and r <= coupling_probability: self.neighbour_positions[p] = positions[p]
        for p in phases:
            if p != self.id and r <= coupling_probability: self.neighbour_phases[p] = phases[p]