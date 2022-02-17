import pygame
import math


class Engine:

    def __init__(self, screen, object_list):
        self.object_list = object_list
        self.screen = screen

    # calculates gravitational force between objects
    def calculate_force(self):
        for p in self.object_list:
            force_list = []
            name = p.get_classification()
            if "asteroid" in p.classification or "Ship" in p.classification:
                for i in self.object_list:
                    if name != i.get_classification():
                        f = self.calculate_object_force([p.mass, i.mass], [[p.get_pos_x(), p.get_pos_y()], [i.get_pos_x(), i.get_pos_y()]], [p.radius, i.radius])
                        force_list.append(f)
                        if "asteroid" in p.classification:
                            p.collision(i.get_radius(), i.mass, [i.get_pos_x(), i.get_pos_y()], i.get_classification(), self.object_list, [i.get_x_force(), i.get_y_force()])
                force = p.calculate_total_force(force_list)
                p.add_total_force(force)
                p.add_new_position()

    # a function that gets called when we calculate force between two objects
    def calculate_object_force(self, mass, coordinates, radius):
        direction = math.atan2(coordinates[1][1] - coordinates[0][1], coordinates[1][0] - coordinates[0][0])
        distance = self.calculate_distance(coordinates)
        if distance > (radius[0] + radius[1]) and distance != 0:
            force = (mass[0] * mass[1]) / math.pow(distance, 2)
        elif distance != 0:
            force = -(mass[0] * mass[1]) / math.pow(distance, 2)
        else:
            force = 0
        x_force = (math.cos(direction)) * force/mass[0]
        y_force = (math.sin(direction)) * force/mass[0]
        return x_force, y_force

    def calculate_distance(self, coordinates):
        distance = math.sqrt(math.pow(coordinates[0][0] - coordinates[1][0], 2) + math.pow(coordinates[0][1] - coordinates[1][1], 2))
        return distance
