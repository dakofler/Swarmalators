import tkinter
import random
import math
import time
from swarmalator_model.swarmalator import Swarmalator


def initialise_canvas(window, screen_size):
    canvas = tkinter.Canvas(window, width=screen_size, height=screen_size)
    canvas.pack()
    window.resizable(False, False)
    return canvas

def create_swarmalators(canvas, no_of_swarmalators):
    list_of_swarmalators = []

    for n in range(no_of_swarmalators):
        swarmalator = Swarmalator("swarmalator" + str(n))
        list_of_swarmalators.append(swarmalator)
        swarmalator.draw_swarmalator(canvas)

    return list_of_swarmalators

def separation(nearest_neighbour, swarmalator):
    # move 1: move away from nearest - separation
    # calculate angle between swarmalator and nearest swarmalator, then angle it in the opposite direction

    if nearest_neighbour is not None and swarmalator.euclidean_distance(nearest_neighbour) < 35:
        if nearest_neighbour.x - swarmalator.x == 0.0:
            angle = math.atan((nearest_neighbour.y - swarmalator.y) / 0.0001)
        else:
            angle = math.atan((nearest_neighbour.y - swarmalator.y) / (nearest_neighbour.x - swarmalator.x))

        swarmalator.angle -= angle

def alignment(neighbours, swarmalator):
    # move 2: orient towards the neighbours - alignment
    # calculate average angle of neighbours and move in that direction

    average_neighbours_angle = 0.0

    if neighbours:
        for neighbour_swarmalator in neighbours:
            average_neighbours_angle += neighbour_swarmalator.angle

        average_neighbours_angle /= len(neighbours)
        swarmalator.angle -= (average_neighbours_angle-swarmalator.angle) / 100.0
        swarmalator.angle = average_neighbours_angle

def cohesion(neighbours, swarmalator):
    # move 3: move together - cohesion

    if neighbours:
        avg_x = 0.0
        avg_y = 0.0

        for neighbour_swarmalator in neighbours:
            avg_x += neighbour_swarmalator.x
            avg_y += neighbour_swarmalator.y

        avg_x /= len(neighbours)
        avg_y /= len(neighbours)

        if avg_x - swarmalator.x == 0.0:
            angle = math.atan((avg_y - swarmalator.y) / 0.00001)
        else:
            angle = math.atan((avg_y - swarmalator.y) / (avg_x - swarmalator.x))

        swarmalator.angle -= angle / 20.0

def swarmalator_behaviours(canvas, list_of_swarmalators, screen_size):
    
    # find neighbours
    for swarmalator in list_of_swarmalators:
        neighbours = []

        for s in list_of_swarmalators:
            # if s is nearby current swarmalator, then it is a neighbour and make sure neighbor swarmalator is not current swarmalator
            if swarmalator.euclidean_distance(s) < 75 and (not swarmalator.euclidean_distance(s) == 0):
                neighbours.append(s)

        nearest_neighbour = None

        # finding nearest neighbour
        if neighbours:
            shortest_distance = 999999999

            for neighbour_swarmalator in neighbours:
                d = swarmalator.euclidean_distance(neighbour_swarmalator)

                if d < shortest_distance:
                    shortest_distance = d
                    nearest_neighbour = neighbour_swarmalator

        separation(nearest_neighbour, swarmalator)
        alignment(neighbours, swarmalator)
        cohesion(neighbours, swarmalator)

    for swarmalator in list_of_swarmalators:
        swarmalator.step(canvas, screen_size)

    canvas.after(25, swarmalator_behaviours, canvas, list_of_swarmalators, screen_size)