import tkinter
from swarmalator_model.swarmalator import Swarmalator

def initialize_canvas(window, screen_size):
    '''Initializes a tikinter canvas.

    Parameters
    ----------
        window (tkinter.Tk): tkinter instance
        screen_size (int): size of the canvas
    
    Returns
    ----------
        canvas (tikinter.Canvas): Canvas object
    '''
    canvas = tkinter.Canvas(window, width=screen_size, height=screen_size)
    canvas.pack()
    window.resizable(False, False)
    return canvas

def create_swarmalators(canvas, no_of_swarmalators, screen_size, memory_init):
    '''Creates swarmalator instances.

    Parameters
    ----------
        canvas (tikinter.Canvas): Canvas object the swarmalators should be added to.
        no_of_swarmalators (int): Number of swarmalators to add to a canvas
        screen_size (int): size of the canas
        memory_init (string): Determines how position and phase memories of swarmalators are initialized. Options: `zero`, `rand`
    
    Returns
    ----------
        list_of_swarmalators (list[swarmalator_model.Swarmalator]): List of swarmalator objects
    '''
    list_of_swarmalators = []

    for n in range(no_of_swarmalators):
        swarmalator = Swarmalator(n, no_of_swarmalators, memory_init)
        list_of_swarmalators.append(swarmalator)
        swarmalator.draw_swarmalator(canvas, screen_size)

    return list_of_swarmalators

def run_simulation(screen_size, no_of_swarmalators, delta_t, J, K, coupling_probability, memory_init = 'rand'):
    '''Initiates the main loop of the simulation.

    Parameters
    ----------
        screen_size (int): size of the canas
        no_of_swarmalators (int): Number of swarmalators to add to a canvas
        delta_t (float): value of one euler step, rate at which the canas updates
        J (float): Parameter that influences the attraction and repulsion between swarmalators
        K (float): Parameter that influences the phase synchronization between swarmalators
        coupling_probability (float): Probability for a swarmalator to update its information about neighbours (default `0.01`)
        memory_init (string): Determines how position and phase memories of swarmalators are initialized. Options: `zero`, `rand` (default `zero`)
    ''' 
    sim = tkinter.Tk()
    canvas = initialize_canvas(sim, screen_size)
    list_of_swarmalators = create_swarmalators(canvas, no_of_swarmalators, screen_size, memory_init)

    step(canvas, list_of_swarmalators, screen_size, delta_t, J, K, coupling_probability)

    sim.mainloop()

def step(canvas, list_of_swarmalators, screen_size, delta_t, J, K, coupling_probability):
    '''Updates the canas and all swarmalators.

    Parameters
    ----------
        canvas (tikinter.Canvas): Canvas object the swarmalators should be added to.
        list_of_swarmalators (list[swarmalator_model.Swarmalator]): List of swarmalator objects
        screen_size (int): size of the canas
        delta_t (float): value of one euler step, rate at which the canas updates
        J (float): Parameter that influences the attraction and repulsion between swarmalators
        K (float): Parameter that influences the phase synchronization between swarmalators
        coupling_probability (float): Probability for a swarmalator to update its information about neighbours (default `0.01`)
    '''    
    canvas.delete("all")

    for swarmalator in list_of_swarmalators:
        swarmalator.step(list_of_swarmalators, delta_t, J, K, coupling_probability)

    for swarmalator in list_of_swarmalators:
        swarmalator.draw_swarmalator(canvas, screen_size)

    delay = int(delta_t * 1000)
    canvas.after(delay, step, canvas, list_of_swarmalators, screen_size, delta_t, J, K, coupling_probability)