from swarmalator_model.dataset import Dataset
import numpy as np
from swarmalator_model import helper_functions as hlp


class Analysis:
    def __init__(self):
        '''
        Instantiates an Analysis object.
        '''
        self.datasets = {}

    def add_dataset(self, dataset: Dataset, name: str):
        '''
        Adds a Dataset object to the datasets dictionary.

        Parameters
        ----------
        dataset : Dataset
            Dataset object to be added to the datasets dictionary.
        name : str
            Name of the dataset to be used as key.
        '''  
        if name in self.datasets:
            print('Name already exists')
            return
        self.datasets[name] = dataset

    def list_datasets(self):
        '''
        Lists the names of all Dataset objects within the datasets dictionary.
        '''  
        for d in self.datasets:
            print(d)

    def plot_avg_speed(self, dataset_name: str):
        '''
        Plots the average speed over all iterations of a Dataset object.

        Parameters
        ----------
        dataset_name : str
            Name of the Dataset object within the datasets dictionary.
        '''  
        if dataset_name not in self.datasets:
            print('Dataset not found.')
            return

        d = self.datasets[dataset_name]
        pos, pha, vel = d.prep_data()
        
        Y = np.average(np.linalg.norm(vel, axis=2), axis=1)
        X = np.arange(1, len(Y) + 1)

        hlp.plot2D(x=X, y=Y, x_label='iteration', y_label='average speed', type='line', title='Average speed per iteration')

        pass


