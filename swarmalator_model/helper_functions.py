import math
import colorsys
import pickle
import plotly.express as px
import pandas as pd
import numpy as np


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

def plot2D(type: str, x: np.ndarray, y: np.ndarray, x_label: str, y_label: str, title: str):
    '''
    Creats a 2D Plot.

    Parameters
    ----------
    type : str
        Plot type. Can be `line` or `scatter`.
    x : nd.ndarray
        Numpy array of x values of shape (n, ).
    y : nd.ndarray
        Numpy array of y values of shape (n, ).
    x_label : str
        X-axis label.
    y_label : str
        Y-axis label.
    title : str
        Plot title.
    '''   
    data = pd.DataFrame({
        x_label : x,
        y_label : y
    })

    if type == 'line':
        fig = px.line(data, x=x_label, y=y_label, title=title)
        fig.show()

    elif type == 'scatter':
        pass
    return