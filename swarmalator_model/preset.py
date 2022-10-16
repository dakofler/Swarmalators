import os
import json

class Preset():
    def __init__(self, preset: dict = None):
        '''
        Instantiates a Preset object.

        Parameters
        ----------
        preset : dict, optional
            Dictionary of parameters to be used in for the preset object.
        '''
        if preset is not None:
            self.dict = preset
            self.num_swarmalators = preset['n']
            self.memory_init = preset['i']
            self.time_step = preset['dt']
            self.J = preset['j']
            self.K = preset['k']
            self.coupling_probability = preset['cp']
            self.alpha = preset['a']
        else:
            self.dict = None

    def save_to_json(self):
        '''
        Saves preset parameters to a JSON-file.
        '''
        if self.dict is None:
            print('No parameters in preset.')
            return

        if not os.path.exists('presets\\'): os.makedirs('presets\\')

        filename = '_'.join([
            str(self.num_swarmalators),
            str(self.memory_init),
            str(self.time_step),
            str(self.coupling_probability),
            str(self.J),
            str(self.K),
            str(self.alpha)
        ])
    
        with open(f'presets\\{filename}.json', 'w') as outfile: json.dump(self.dict, outfile)

    def load_from_json(self, filename: str):
        '''
        Loads preset parameters from a JSON-file.

        Parameters
        ----------
        filename : str
            Filename of the JSON-file containing parameters to load.
        '''
        filepath = f'presets\\{filename}'
        if not os.path.exists(filepath):
            print(f'Preset-file {filepath} not found.')
            return

        with open(filepath) as json_file: data = json.load(json_file)

        self.dict = data
        self.num_swarmalators = data['n']
        self.memory_init = data['i']
        self.time_step = data['dt']
        self.J = data['j']
        self.K = data['k']
        self.coupling_probability = data['cp']
        self.alpha = data['a']

    def summary(self):
        '''
        Prints information about the Preset object.
        '''
        print(f'Number of swarmalators: {self.num_swarmalators}')
        print(f'Memory initialization: {self.memory_init}')
        print(f'Time step: {self.time_step}s')
        print(f'J: {self.J}')
        print(f'K: {self.K}')
        print(f'Coupling probabiltity: {self.coupling_probability}')
        print(f'Alpha: {self.alpha}')