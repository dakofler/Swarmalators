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
            memory_positions = np.random.rand(num_swarmalators, 2) * 2.0 - 1.0 #position-array
            memory_phases = np.random.rand(num_swarmalators) * 2.0 * math.pi #phase-vector
            memory_phases = memory_phases.reshape((num_swarmalators, 1))
            self.memory = np.concatenate((memory_positions, memory_phases), axis=1)
        else:
            self.info = np.zeros((num_swarmalators, 3)) #position-phase-array

            # initialize own position and phase randomly
            self.memory[self.id][0] = rnd.random() * 2.0 - 1.0
            self.memory[self.id][1] = rnd.random() * 2.0 - 1.0
            self.memory[self.id][2] = rnd.uniform(0.0, 2.0 * math.pi)
       
    def run(self, env_memory, env_velocities, delta_t, J, K, coupling_probability):
        self.scan(env_memory, coupling_probability)
        self.think(J, K)
        self.move(delta_t)
        self.yell(env_memory, env_velocities)

    def move(self, delta_t):
        self.memory[self.id][:2] = self.memory[self.id][:2]  + self.velocity * delta_t # compute next position the swarmalator moves to
        self.memory[self.id][2] = (self.memory[self.id][2] + self.d_phase * delta_t) % (2.0 * math.pi) # update phase
    
    def think(self, J, K):
        v_temp = np.zeros(2)
        p_temp = 0.0

        for i in range(self.num_swarmalators):
            if i != self.id:
                d_position = self.memory[i][:2] - self.memory[self.id][:2]
                d_phase = self.memory[i][2] - self.memory[self.id][2]
                d_pos_norm = np.linalg.norm(d_position)
                
                v_temp += d_position / d_pos_norm * ((1.0 + J * math.cos(d_phase)) - 1.0 / d_pos_norm)
                p_temp += math.sin(d_phase) / d_pos_norm

        self.velocity = 1 / self.num_swarmalators * v_temp
        self.d_phase = K / self.num_swarmalators * p_temp

    def scan(self, memory, coupling_probability):
        for i in range(self.num_swarmalators):
            if i != self.id:
                r = rnd.random()
                if r <= coupling_probability:
                    self.memory[i] = memory[i]
    
    def yell(self, env_memory, env_velocities):
        env_memory[self.id] = self.memory[self.id]
        env_velocities[self.id] = self.velocity