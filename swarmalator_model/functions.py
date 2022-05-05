import tkinter, threading, math, colorsys, time
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

    return list_of_swarmalators

def initialize_status(list_of_swarmalators):
    '''Fills the global position an phase dict.

    Parameters
    ----------
        list_of_swarmalators (list[swarmalator_model.Swarmalator]): List of swarmalator objects
    
    Returns
    ----------
        positions (dict): Positions of swarmaltors in the system.
        phases (dict): Phases of swarmaltors in the system.
    '''
    positions = {}
    phases = {}

    for s in list_of_swarmalators:
        positions[s.id] = s.position
        phases[s.id] = s.phase

    return positions, phases

def update_status(list_of_swarmalators, positions, phases):
    '''Updates the global position an phase dicts.

    Parameters
    ----------
        list_of_swarmalators (list[swarmalator_model.Swarmalator]): List of swarmalator objects
        positions (dict): Positions of swarmaltors in the system.
        phases (dict): Phases of swarmaltors in the system.
    '''
    for s in list_of_swarmalators:
        positions[s.id] = s.position
        phases[s.id] = s.phase

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
    sim.title('Swarmalators with Stochastic Coupling 2022 D. Kofler')
    canvas = initialise_canvas(sim, screen_size)
    list_of_swarmalators = create_swarmalators(canvas, no_of_swarmalators, screen_size)
    positions, phases = initialize_status(list_of_swarmalators)

    draw_swarmalators(canvas, screen_size, positions, phases)

    step(canvas, list_of_swarmalators, positions, phases, screen_size, delta_t, J, K, coupling_probability)
    sim.mainloop()

def step(canvas, list_of_swarmalators, positions, phases, screen_size, delta_t, J, K, coupling_probability):
    '''Updates the canas and all swarmalators.

    Parameters
    ----------
        canvas (tikinter.Canvas): Canvas object the swarmalators should be added to.
        positions (dict): Positions of swarmaltors in the system.
        phases (dict): Phases of swarmaltors in the system.
        screen_size (int): size of the canas
        delta_t (float): value of one euler step, rate at which the canas updates
        J (float): Parameter that influences the attraction and repulsion between swarmalators
        K (float): Parameter that influences the phase synchronization between swarmalators
        coupling_probability (float): Probability for a swarmalator to update its information about neighbours (default `0.01`)
    '''    
    canvas.delete("all")
    threads = []

    start = time.time()  
    for swarmalator in list_of_swarmalators:
        # swarmalator.step(positions, phases, delta_t, J, K, coupling_probability)
        t = threading.Thread(target=swarmalator.step, args=(positions, phases, delta_t, J, K, coupling_probability), daemon=True)
        threads.append(t)
        t.start()

    for t in threads:
        t.join()
    
    update_status(list_of_swarmalators, positions, phases)
    draw_swarmalators(canvas, screen_size, positions, phases)
    end = time.time()
    calc_time = end - start
    print(f'calc time {calc_time} s ...')

    delay = int(delta_t * 1000 - calc_time)
    canvas.after(delay, step, canvas, list_of_swarmalators, positions, phases, screen_size, delta_t, J, K, coupling_probability)

def draw_swarmalators(canvas, screen_size, positions, phases):
    '''Draws all swarmalators on the canvas.

    Parameters
    ----------
        canvas (tikinter.Canvas): Canvas object the swarmalators should be added to.
        screen_size (int): size of the canvas
        positions (dict): Positions of swarmaltors in the system.
        phases (dict): Phases of swarmaltors in the system.

    '''
    size = 10

    for p in positions:
        # color based on swarmalator phase
        c_val = phases[p] / (2.0 * math.pi) % (2.0 * math.pi)
        c_rgb = colorsys.hsv_to_rgb(c_val, 1, 1)
        c_int = tuple(int(t * 255) for t in c_rgb)
        c_hex = '#%02x%02x%02x' % c_int

        pos = positions[p]
        canv_pos_x = pos[0] * screen_size / 4 + screen_size / 2
        canv_pos_y = pos[1] * screen_size / 4 + screen_size / 2
        x1 = canv_pos_x + size
        x2 = canv_pos_y + size

        canvas.create_oval(canv_pos_x, canv_pos_y, x1, x2, fill=c_hex, tags=p)