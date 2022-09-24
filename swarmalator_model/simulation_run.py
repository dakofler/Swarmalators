from swarmalator_model.simulation import Simulation

class Simulation_run:
    def __init__(self, presets: list, sim_time: int):
        '''
        Instantiates a simulation run object.

        Parameters
        ----------
        preset : list
            List of preset objects.
        sim_time : int
            Time in s a simulation should run for.
        '''
        self.presets = presets
        self.sim_time = sim_time

    def start(self):
        '''
        Starts a simulation run.
        '''
        for i, p in enumerate(self.presets):
            sim = None
            parameters = {}
            parameters = p.dict

            sim = Simulation(
                plot_size=750,
                logging=True,
                num_swarmalators=parameters['n'],
                memory_init=parameters['i'],
                coupling_probability=parameters['cp'],
                J=parameters['j'],
                K=parameters['k'],
                alpha=parameters['a'],
                max_simulation_time=self.sim_time,
                auto=True)
            sim.run_simulation()

            print(f'Run {i + 1} completed successfully.')
        print(f'All runs completed.')
