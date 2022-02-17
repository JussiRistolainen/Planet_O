import random
import math
from planet import Planet
from sun import Sun
from asteroid import Asteroid
from ship import Ship


class World:

    def __init__(self, screen,  object_list, zoom):
        self.screen = screen
        self.object_list = object_list
        self.index_p = 0
        self.index_m = 0
        self.index_s = 0
        self.index_a = 0
        self.zoom = zoom

    # creates a sun object
    def create_sun(self, number, position, size):
        for k in range(number):
            radius = random.randint(12, 18)
            y = random.randint(position[1], position[1]+size)
            x = random.randint(position[0], position[1]+size)
            K = Sun(self.screen, x, y, radius, 100, "Sun" + str(self.index_s), self.zoom)
            self.object_list.append(K)
            self.index_s += 1

    # creates a planet object around a specific sun with a number of moons
    def create_planet_with_moon(self, number_planet, number_moon, sun_name):
        for i in self.object_list:
            if i.get_classification() == sun_name:
                sun = i
        for i in range(number_planet):
            radius = random.randint(9, 12)
            size = random.randint(1, 3)
            y_axis = random.randint(size * 100, size * 120)
            x_axis = random.randint(size * 120, size * 140)
            angle = random.uniform(0, math.pi)
            A = Planet(self.screen, 100, angle, angle, radius, x_axis, y_axis, sun, "planet"+str(self.index_p), 0, 0, self.zoom)
            self.object_list.append(A)
            self.index_p += 1
            for i in range(number_moon):
                radius = random.randint(3, 6)
                size = random.randint(2, 4)
                y_axis = random.randint(size * 10, size * 11)
                x_axis = random.randint(size * 11, size * 12)
                angle = random.uniform(0, math.pi)
                B = Planet(self.screen, 100, angle, angle, radius, x_axis, y_axis, A, "planet" + str(self.index_m), 0, 0, self.zoom)
                self.object_list.append(B)
                self.index_m += 1

    # creates asteroid objects
    def create_asteroid(self, number_asteroid):
        for i in range(number_asteroid):
            y = random.randint(100, 600)
            x = random.randint(100, 600)
            B = Asteroid(self.screen, 100, 5, x, y, "asteroid"+str(self.index_a), self.zoom)
            self.object_list.append(B)
            self.index_a += 1

    # creates a ship object
    def create_ship(self, position):
        B = Ship(self.screen, 100, 5, position[0], position[1], "SpaceShip", self.zoom)
        self.object_list.append(B)
        return B

