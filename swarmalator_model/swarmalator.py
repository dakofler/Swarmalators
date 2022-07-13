import random as rnd
import math
import numpy as np
import time


class Swarmalator:
    def __init__(self, id, num_swarmalators, memory_init):
        self.id = id
        self.num_swarmalators = num_swarmalators

        self.velocity = np.ones(2)
        self.d_phase = 0

        # initialize memories with random values
        if memory_init == 'rand':
            self.phases = np.random.rand(num_swarmalators) * 2.0 * math.pi #phase-vector
            self.positions = np.random.rand(num_swarmalators, 2) * 2.0 - 1.0 #position-array
        else:
            self.phases = np.zeros(num_swarmalators) #phase-vector
            self.positions = np.zeros((num_swarmalators, 2)) #position-vector

            # initialize own position and phase randomly
            self.positions[self.id][0] = rnd.random() * 2.0 - 1.0
            self.positions[self.id][1] = rnd.random() * 2.0 - 1.0
            self.phases[self.id] = rnd.uniform(0.0, 2.0 * math.pi)           
       
    def run(self, positions, phases, velocities, delta_t, J, K, coupling_probability):
        # while true:
            self.scan(positions, phases, coupling_probability)
            self.think(J, K)
            self.move(delta_t)
            self.yell(positions, phases, velocities)
            # time.sleep(delta_t)

    def move(self, delta_t):  
        self.positions[self.id] = self.positions[self.id] + self.velocity * delta_t # compute next position the swarmalator moves to
        self.phases[self.id] = (self.phases[self.id] + self.d_phase * delta_t) % (2.0 * math.pi) # update phase
    
    def think(self, J, K):
        v_temp = np.zeros(2)
        p_temp = 0.0

        for i in range(self.num_swarmalators):
            if i != self.id:
                d_x = self.positions[i] - self.positions[self.id]
                d_theta = self.phases[i] - self.phases[self.id]
                d_x_norm = np.linalg.norm(d_x)
                
                v_temp += d_x / d_x_norm * ((1.0 + J * math.cos(d_theta)) - 1.0 / d_x_norm)
                p_temp += math.sin(d_theta) / d_x_norm

        self.velocity = 1 / self.num_swarmalators * v_temp
        self.d_phase = K / self.num_swarmalators * p_temp

    def scan(self, positions, phases, coupling_probability):
        for i in range(self.num_swarmalators):
            if i != self.id:
                r = rnd.random()
                if r <= coupling_probability:
                    self.positions[i] = positions[i]
                    self.phases[i] = phases[i]
    
    def yell(self, positions, phases, velocities):
        positions[self.id] = self.positions[self.id]
        phases[self.id] = self.phases[self.id]
        velocities[self.id] = self.velocity