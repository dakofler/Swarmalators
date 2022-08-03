import pickle
from datetime import datetime


class Dataset():
    def __init__(self, data: list):
        self.memory = data[0]
        self.velocities = data[1]

    def save_to_file(self):
        filename = 'sim_data\\dataset_' + datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        with open(filename, 'wb') as fp:
            pickle.dump(self, fp)