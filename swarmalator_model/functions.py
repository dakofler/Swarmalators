import numpy as np
import colorsys


def phase_to_hex(phase: float):
    '''
    Returns a hex color code based on an input phase value.

    Parameters
    ----------
    phase : float
        Phase-value in the range [0 : 2*PI]

    Returns
    ----------
    string
        Hex color code
    '''
    c_val = phase / (2.0 * np.pi)
    c_rgb = colorsys.hsv_to_rgb(c_val, 1, 1)
    c_int = tuple(int(t * 255) for t in c_rgb)
    return '#%02x%02x%02x' % c_int
