import pickle
import os
from datetime import datetime


class Dataset():
    def __init__(self, data: list):
        self.memory = data[0]
        self.velocities = data[1]
        self.sim_time = data[2]

    def save_to_file(self):
        if not os.path.exists('sim_data\\'): os.makedirs('sim_data\\')
        filename = 'sim_data\\dataset_' + datetime.now().strftime('%Y-%m-%d_%H-%M-%S') + '.ssd'
        with open(filename, 'wb') as fp:
            pickle.dump(self, fp)
    
    def summary(self):
        print(f'Number of swarmalators: {len(self.memory[0])}')
        print(f'Simulation iterations: {len(self.memory)}')
        print(f'Simulation time: {self.sim_time}s')
