from swarmalator_model.dataset import Dataset

class Analysis:
    def __init__(self, dataset: Dataset):
        self.dataset = dataset

    def extract_data(self):
        self.positions = self.dataset.memory[:, :2]
        print(self.positions)
    
    # ToDo