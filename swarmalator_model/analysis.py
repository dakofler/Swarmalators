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

    def plot_avg_speed(self, dataset_names: list, save: bool = False):
        '''
        Plots the average speed over all iterations of Dataset objects.

        Parameters
        ----------
        dataset_names : list
            List of Dataset object names within the datasets dictionary.
        save : bool, optional
            Whether to save to plot as .jpg. default=False
        '''

        data = {}

        for d in dataset_names:
            if d not in self.datasets:
                print(f'Dataset {d} not found.')
                return
            
            ds = self.datasets[d]
            pos, pha, vel = ds.prep_data()
            y = np.average(np.linalg.norm(vel, axis=2), axis=1)
            x = np.arange(1, len(y) + 1)

            data[d] = [x, y]

        hlp.plot_lines(data=data, x_label='Iteration', y_label='Average Speed in Units/Timestep', title='Average Speed per Iteration', save=save)


