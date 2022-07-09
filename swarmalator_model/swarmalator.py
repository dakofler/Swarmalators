import random as rnd
import math
import numpy as np

class Swarmalator:
    def __init__(self, id, num_of_swarmalators):
        '''Creates a swarmalator instance.

        Parameters
        ----------
            id (str): id of the swarmalator.
            phase (float): pahse of the swarmalator (default `None`)
        '''
        self.id = id

        self.velocity = np.zeros(2)
        self.d_phase = 0
<<<<<<< HEAD

        self.phases = np.zeros(num_of_swarmalators) #phase-vector
        self.positions = np.zeros((num_of_swarmalators, 2)) #position-array
        
        self.phases[self.id] = rnd.uniform(0.0, 2.0 * math.pi)

        self.positions[self.id][0] = rnd.random() * 2 - 1 # x-position
        self.positions[self.id][1] = rnd.random() * 2 - 1 # y-position
       
    def draw_swarmalator(self, canvas, screen_size):
        '''Adds the swarmalator to a canvas instance.

        Parameters
        ----------
            canvas (tikinter.Canvas): Canvas object the swarmalators should be added to.
            screen_size (int): size of the canvas
        '''
        size = 10

        # color based on swarmalator phase
        c_val = self.phases[self.id] / (2.0 * math.pi) % (2.0 * math.pi)
        c_rgb = colorsys.hsv_to_rgb(c_val, 1, 1)
        c_int = tuple(int(t * 255) for t in c_rgb)
        c_hex = '#%02x%02x%02x' % c_int

        canv_pos_x = self.positions[self.id][0] * screen_size / 4 + screen_size / 2
        canv_pos_y = self.positions[self.id][1] * screen_size / 4 + screen_size / 2
        x1 = canv_pos_x + size
        x2 = canv_pos_y + size

        canvas.create_oval(canv_pos_x, canv_pos_y, x1, x2, fill=c_hex, tags='s' + str(self.id))

    def step(self, list_of_swarmalators, delta_t, J, K, coupling_probability):
=======
        self.neighbour_phases = {}
        self.neighbour_positions = {}

    def step(self, positions, phases, delta_t, J, K, coupling_probability):
>>>>>>> 347b629196238f5cbec67f52fe036be96e460b18
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
<<<<<<< HEAD
        self.synchronize(list_of_swarmalators, coupling_probability)
        self.update(len(list_of_swarmalators), J, K)
=======
        self.synchronize(positions, phases, coupling_probability)
        self.think(positions, phases, J, K)
>>>>>>> 347b629196238f5cbec67f52fe036be96e460b18
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
    
<<<<<<< HEAD
    def update(self, num_of_swarmalators, J, K):
        '''Updates the position and phase of a swarmalator based on it's neighbours.
=======
    def think(self, positions, phases, J, K):
        '''Updates the position and pahse of a swarmalator based on it's neighbours.
>>>>>>> 347b629196238f5cbec67f52fe036be96e460b18

        Parameters
        ----------
            list_of_swarmalators (list[swarmalator_model.Swarmalator]): List of swarmalator objects
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

<<<<<<< HEAD
        self.velocity = 1 / (len(self.positions)) * v_temp
        self.d_phase = K / (len(self.phases)) * p_temp
=======
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
>>>>>>> 347b629196238f5cbec67f52fe036be96e460b18

    def synchronize(self, positions, phases, coupling_probability):
        '''Updates a swarmalator's memory of positions and phases of it's neighbours.

        Parameters
        ----------
            list_of_swarmalators (list[swarmalator_model.Swarmalator]): List of swarmalator objects
            coupling_probability (float): Probability for a swarmalator to update its information about neighbours
        '''
<<<<<<< HEAD
        for i in range(len(self.positions)):
            if i != self.id:
                r = rnd.random()
                if r <= coupling_probability:
                    self.positions[i] = list_of_swarmalators[i].positions[i]
                    self.phases[i] = list_of_swarmalators[i].phases[i]
=======
        r = rnd.random()
        for p in positions:
            if p != self.id and r <= coupling_probability: self.neighbour_positions[p] = positions[p]
        for p in phases:
            if p != self.id and r <= coupling_probability: self.neighbour_phases[p] = phases[p]
>>>>>>> 347b629196238f5cbec67f52fe036be96e460b18
