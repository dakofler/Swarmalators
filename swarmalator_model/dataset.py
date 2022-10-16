import pickle
import os
from sqlite3 import Time
import numpy as np
from datetime import datetime


class Dataset():
    def __init__(self, data: list):
        '''
        Instantiates a Dataset object.

        Parameters
        ----------
        data : list
            List of data to be loaded into the Dataset object.
        '''
        if len(data) != 4:
            print('Dataset outdated')
            return
        self.positions = np.array(data[0])[:, :, :2].tolist()
        self.phases =  np.array(data[0])[:, :, 2].tolist()
        self.velocities = data[1]
        self.sim_time = data[2]
        self.parameters = data[3]
        self.identifier = '_'.join([
            str(self.parameters['n']),
            self.parameters['i'],
            str(self.parameters['dt']),
            str(self.parameters['cp']),
            str(self.parameters['j']),
            str(self.parameters['k']),
            str(self.parameters['a']),
            str(datetime.now().strftime('%Y%m%d%H%M%S'))])

    def save_to_file(self):
        '''
        Saves the Dataset object to a binary file using pickle.
        '''
        if not os.path.exists('sim_data\\'): os.makedirs('sim_data\\')
        filename = 'sim_data\\' + self.identifier + '.ssd'
        with open(filename, 'wb') as fp:
            pickle.dump(self, fp)
    
    def summary(self):
        '''
        Prints information about the Dataset object.
        '''
        print(f'Number of swarmalators: {len(self.positions[0])}')
        print(f'Simulation iterations: {len(self.positions)}')
        print(f'Simulation time: {self.sim_time}s')
        print(f'Time step: {self.parameters["dt"]}s')
        print(f'J: {self.parameters["j"]}')
        print(f'K: {self.parameters["k"]}')
        print(f'Coupling probabiltity: {self.parameters["cp"]}')
        print(f'alpha: {self.parameters["a"]}')
    
    def prep_data(self):
        '''
        Converts data into numpy arrays for analysis.

        Retruns
        ----------
        positions : np.ndarray
            Numpy array with swarmalator positions of shape (n, 2)
        phases : np.ndarray
            Numpy array with swarmalator phases of shape (n, )
        velocities : np.ndarray
            Numpy array with swarmalator velocities of shape (n, 2)
        '''
        positions = np.array(self.positions)
        phases = np.array(self.phases)
        velocities = np.array(self.velocities)
        return positions, phases, velocities
