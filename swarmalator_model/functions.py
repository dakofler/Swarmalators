from ast import arg
from concurrent.futures import thread
import tkinter, threading, time
from swarmalator_model.swarmalator import Swarmalator

def initialise_canvas(window, screen_size):
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

def create_swarmalators(canvas, no_of_swarmalators, screen_size):
    '''Creates swarmalator instances.

    Parameters
    ----------
        canvas (tikinter.Canvas): Canvas object the swarmalators should be added to.
        no_of_swarmalators (int): Number of swarmalators to add to a canvas
        screen_size (int): size of the canas
    
    Returns
    ----------
        list_of_swarmalators (list[swarmalator_model.Swarmalator]): List of swarmalator objects
    '''
    list_of_swarmalators = []

    for n in range(no_of_swarmalators):
        swarmalator = Swarmalator(n)
        list_of_swarmalators.append(swarmalator)
        swarmalator.draw_swarmalator(canvas, screen_size)

    return list_of_swarmalators

def run_simulation(screen_size, no_of_swarmalators, delta_t, J, K, coupling_probability):
    '''Initiates the main loop of the simulation.

    Parameters
    ----------
        screen_size (int): size of the canas
        no_of_swarmalators (int): Number of swarmalators to add to a canvas
        delta_t (float): value of one euler step, rate at which the canas updates
        J (float): Parameter that influences the attraction and repulsion between swarmalators
        K (float): Parameter that influences the phase synchronization between swarmalators
        coupling_probability (float): Probability for a swarmalator to update its information about neighbours (default `0.01`)
    ''' 
    sim = tkinter.Tk()
    canvas = initialise_canvas(sim, screen_size)
    list_of_swarmalators = create_swarmalators(canvas, no_of_swarmalators, screen_size)

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
    threads = []

    for swarmalator in list_of_swarmalators:
        t = threading.Thread(target=swarmalator.step, args=(list_of_swarmalators, canvas, screen_size, delta_t, J, K, coupling_probability), daemon=True)
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    for swarmalator in list_of_swarmalators:
        swarmalator.draw_swarmalator(canvas, screen_size)

    delay = int(delta_t * 1000)
    canvas.after(delay, step, canvas, list_of_swarmalators, screen_size, delta_t, J, K, coupling_probability)