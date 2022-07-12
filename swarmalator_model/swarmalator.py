import random as rnd
import math
import numpy as np

class Swarmalator:
    def __init__(self, id, num_swarmalators, memory_init):
        self.id = id
        self.num_swarmalators = num_swarmalators

        self.velocity = np.ones(2)
        self.d_phase = 0

        # initialize memories with random values
        if memory_init == 'rand':
            self.phases = np.random.rand(num_swarmalators) * 2 * math.pi #phase-vector
            self.positions = np.random.rand(num_swarmalators, 2) * 2 - 1 #position-array
        else:
            self.phases = np.zeros(num_swarmalators) #phase-vector
            self.positions = np.zeros((num_swarmalators, 2)) #position-vector

            # initialize own position and phase randomly
            self.positions[self.id][0] = rnd.random() * 2 - 1
            self.positions[self.id][1] = rnd.random() * 2 - 1
            self.phases[self.id] = rnd.uniform(0.0, 2.0 * math.pi)           
       
    def run(self, list_of_swarmalators, positions, phases, delta_t, J, K, coupling_probability):
        self.scan(list_of_swarmalators, coupling_probability)
        self.think(J, K)
        self.move(delta_t)
        self.yell(positions, phases)

    def move(self, delta_t):  
        self.positions[self.id] = self.positions[self.id] + self.velocity * delta_t # compute next position the swarmalator moves to
        self.phases[self.id] = (self.phases[self.id] + self.d_phase * delta_t) % (2.0 * math.pi) # update phase
    
    def think(self, J, K):
        v_temp = np.zeros(2)
        p_temp = 0.0

        for i in range(len(self.positions)):
            if i != self.id:
                d_x = self.positions[i] - self.positions[self.id]
                d_theta = self.phases[i] - self.phases[self.id]
                d_x_norm = np.linalg.norm(d_x)
                
                v_temp += (d_x / d_x_norm * (1.0 + J * math.cos(d_theta)) - d_x / (d_x_norm * d_x_norm))
                p_temp += math.sin(d_theta) / d_x_norm

        self.velocity = 1 / (len(self.positions)) * v_temp
        self.d_phase = K / (len(self.phases)) * p_temp

    def scan(self, list_of_swarmalators, coupling_probability):
        for i in range(len(self.positions)):
            if i != self.id:
                r = rnd.random()
                if r <= coupling_probability:
                    self.positions[i] = list_of_swarmalators[i].positions[i]
                    self.phases[i] = list_of_swarmalators[i].phases[i]
    
    def yell(self, positions, phases):
        positions[self.id] = self.positions[self.id]
        phases[self.id] = self.phases[self.id]