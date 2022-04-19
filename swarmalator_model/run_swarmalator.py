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
        swarmalator = Swarmalator(n, screen_size)
        list_of_swarmalators.append(swarmalator)
        swarmalator.draw_swarmalator(canvas)

    return list_of_swarmalators

def step(canvas, list_of_swarmalators, screen_size, delta_t, J, K, coupling_probability = 0.01):
    for swarmalator in list_of_swarmalators:
        compute_speed(list_of_swarmalators, swarmalator, J)
        compute_phase(list_of_swarmalators, swarmalator, K)
        synchronize(list_of_swarmalators, swarmalator, coupling_probability)

        swarmalator.update(canvas, screen_size, delta_t)

    # print('step')
    time.sleep(delta_t)

    # loop
    canvas.after(10, step, canvas, list_of_swarmalators, screen_size, delta_t, J, K, coupling_probability)

def compute_speed(list_of_swarmalators, swarmalator, J):
    s_i = swarmalator

    if s_i.swarm_positions and s_i.swarm_phases:
        s_i_pos = np.array([swarmalator.x, swarmalator.y])
        v_temp = np.array([0.0, 0.0])

        for j in list_of_swarmalators:
            if j.id != s_i.id:
                s_j_pos = s_i.swarm_positions[j.id]
                s_j_phase = s_i.swarm_phases[j.id]
                
                dif = s_j_pos - s_i_pos
                norm = np.linalg.norm(dif)

                v_temp += (dif / norm * (1000 + J * math.cos(s_j_phase - s_i.phase)) - dif / (norm * norm))

        v = 1 / (len(s_i.swarm_positions)) * v_temp
        s_i.speed = np.linalg.norm(v)
        s_i.angle = math.atan2(v[1], v[0])

def compute_phase(list_of_swarmalators, swarmalator, K):
    s_i = swarmalator

    if s_i.swarm_positions and s_i.swarm_phases:
        s_i_pos = np.array([s_i.x, s_i.y])
        s_i_phase = s_i.phase
        p_temp = 0.0

        for j in list_of_swarmalators:
            if j.id != s_i.id:
                s_j_pos = s_i.swarm_positions[j.id]
                s_j_phase = s_i.swarm_phases[j.id]
                
                norm = np.linalg.norm(s_j_pos - s_i_pos)

                p_temp += math.sin(s_j_phase - s_i_phase) / norm

        p = K / (len(s_i.swarm_phases)) * p_temp
        s_i.d_phase = p

def synchronize(list_of_swarmalators, swarmalator, coupling_probability):
    for s in list_of_swarmalators:
        if s.id != swarmalator.id:
            # if rnd.random() < coupling_probability:
            swarmalator.swarm_positions[s.id] = np.array([s.x, s.y])
            swarmalator.swarm_phases[s.id] = s.phase