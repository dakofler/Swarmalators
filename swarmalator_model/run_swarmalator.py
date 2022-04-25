import tkinter
import random as rnd
import math
from swarmalator_model.swarmalator import Swarmalator
import numpy as np
import time


def initialise_canvas(window, screen_size):
    canvas = tkinter.Canvas(window, width=screen_size, height=screen_size)
    canvas.pack()
    window.resizable(False, False)
    return canvas

def create_swarmalators(canvas, no_of_swarmalators, screen_size):
    list_of_swarmalators = []

    for n in range(no_of_swarmalators):
        swarmalator = Swarmalator(n)
        list_of_swarmalators.append(swarmalator)
        swarmalator.draw_swarmalator(canvas, screen_size)

    return list_of_swarmalators

def step(canvas, list_of_swarmalators, screen_size, delta_t, J, K, coupling_probability = 0.01, animation_speed=1):
    for swarmalator in list_of_swarmalators:
        update(list_of_swarmalators, swarmalator, J, K)
        synchronize(list_of_swarmalators, swarmalator, coupling_probability)

        swarmalator.move(canvas, screen_size, delta_t)

    # loop
    delay = int(delta_t * 1000)
    canvas.after(delay, step, canvas, list_of_swarmalators, screen_size, delta_t, J, K, coupling_probability)

def update(list_of_swarmalators, swarmalator_i, J, K):
    if swarmalator_i.neighbour_positions and swarmalator_i.neighbour_phases:
        x_i = swarmalator_i.position
        theta_i = swarmalator_i.phase

        v_temp = np.array([0.0, 0.0])
        p_temp = 0.0

        for swarmalator_j in list_of_swarmalators:
            if swarmalator_j.id != swarmalator_i.id:
                x_j = swarmalator_i.neighbour_positions[swarmalator_j.id]
                theta_j = swarmalator_i.neighbour_phases[swarmalator_j.id]
                
                d_x = x_j - x_i
                d_theta = theta_j - theta_i
                d_x_norm = np.linalg.norm(d_x)
                
                v_temp += (d_x / d_x_norm * (1.0 + J * math.cos(d_theta)) - d_x / (d_x_norm * d_x_norm))
                p_temp += math.sin(d_theta) / d_x_norm

        swarmalator_i.velocity = 1 / (len(swarmalator_i.neighbour_positions)) * v_temp
        swarmalator_i.d_phase = K / (len(swarmalator_i.neighbour_phases)) * p_temp

def synchronize(list_of_swarmalators, swarmalator, coupling_probability=1):
    for s in list_of_swarmalators:
        if s.id != swarmalator.id:
            swarmalator.neighbour_positions[s.id] = s.position
            swarmalator.neighbour_phases[s.id] = s.phase