from swarmalator_model.dataset import Dataset
import numpy as np
import matplotlib.pyplot as plt

class Analysis:
    def __init__(self, dataset: Dataset):
        self.dataset = dataset
        self.extract_data()

    def extract_data(self):
        self.positions = np.array(self.dataset.memory)[:, :, :2]
        self.phases = np.array(self.dataset.memory)[:, :, 2]
        self.velocities = np.array(self.dataset.velocities)
    
    def plot_avg_velocity(self):
        y = np.average(np.linalg.norm(self.velocities, axis=2), axis=1).tolist()
        x = np.arange(1, len(y) + 1)
        plt.plot(x, y)