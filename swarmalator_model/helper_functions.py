import math
import colorsys
import pickle
import os
import matplotlib.pyplot as plt


def phase_to_hex(phase: float):
    '''
    Returns a hex color code based on an input phase value.

    Parameters
    ----------
    phase : float
        Phase-value in the interval (0, 2*PI)

    Returns
    ----------
    hex_code : string
        Hex color code
    '''
    c_val = (phase + math.pi) / (2.0 * math.pi)
    c_rgb = colorsys.hsv_to_rgb(c_val, 1, 1)
    c_int = tuple(int(t * 255) for t in c_rgb)
    return '#%02x%02x%02x' % c_int

def load_data(filename: str):
    '''
    Loads data from an .ssd file into a Dataset object.

    Parameters
    ----------
    filename : str
        Name of the file containing a dataset.
        
    Returns
    ----------
    dataset : Dataset
        Dataset object.
    '''  
    with open(filename, 'rb') as fp:
        dataset = pickle.load(fp)
    return dataset


def plot_lines(data: dict, x_label: str, y_label: str, title: str, save: bool = False):
    '''
    Creats a 2D plot with two lines.

    Parameters
    ----------
    data : dict
        Dictionary of traces to be plotted of the form { tracename : [X, Y]}
    x_label : str
        X-axis label.
    y_label : str
        Y-axis label.
    title : str
        Plot title.
    save : bool, optional
        Whether to save to plot as .jpg. default=False
    '''   
    if save and not os.path.exists('plots\\'): os.makedirs('plots\\')

    plt.figure(figsize=(10, 6))

    filename = ''

    for trace in data:
        x = data[trace][0]
        y = data[trace][1]
        plt.plot(x, y, label=trace)
        filename += (('_' + trace) if filename != '' else trace)

    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(title)
    plt.grid(axis='y')
    plt.legend()
    if save: plt.savefig(f'plots\\{filename}.jpg')
    else: plt.show()