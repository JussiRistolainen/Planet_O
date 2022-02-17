import math
import pygame
from numpy import random


class Equations:

    def __init__(self, screen, radius, density, classification, position_x, position_y, zoom):
        self.screen = screen
        self.radius = radius
        self.density = density
        self.classification = classification
        self.color = self.calculate_color()
        self.x_force = 0
        self.y_force = 0
        self.mass = self.calculate_mass()
        self.position_x = position_x
        self.position_y = position_y
        self.zoom = zoom

    def calculate_mass(self):
        return (4/3) * math.pi * math.pow(self.radius, 3) * self.density

    def calculate_color(self):
        red = random.randint(255)
        green = random.randint(255)
        blue = random.randint(255)
        return [red, green, blue]

    # long list of get functions
    def get_classification(self):
        return self.classification

    def get_radius(self):
        return self.radius

    def get_x_force(self):
        return self.x_force

    def get_y_force(self):
        return self.y_force

    def set_x_force(self, number):
        self.x_force = number

    def set_y_force(self, number):
        self.y_force = number

    def set_screen(self, screen):
        self.screen = screen

    def set_zoom(self, zoom):
        self.zoom = zoom

    def get_pos_x(self):
        return self.position_x

    def get_pos_y(self):
        return self.position_y
