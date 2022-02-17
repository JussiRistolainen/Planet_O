import math
from equations import Equations
import random


class Asteroid(Equations):

    def __init__(self, screen, density, radius, position_x, position_y, classification, zoom):
        super(Asteroid, self).__init__(screen, radius, density, classification, position_x, position_y, zoom)

    def calculate_distance(self, coordinates):
        distance = math.sqrt(math.pow(self.position_x - coordinates[0], 2) + math.pow(self.position_y - coordinates[1], 2))
        return distance

    # Calculates if objects collide and uses other functions to either destroy or combine the asteroids
    def collision(self, radius, mass, coordinates, name, object_list, force):
        distance = self.calculate_distance(coordinates)
        destroyed = []
        if distance < (radius + self.radius-3):
            for p, i in enumerate(object_list):
                if "asteroid" in i.get_classification() and "asteroid" in name:
                    if i.get_classification() == self.get_classification() or i.get_classification() == name:
                        object_list.pop(p)
                elif i.get_classification() == self.get_classification():
                    object_list.pop(p)
            if "asteroid" in self.get_classification() and "asteroid" in name:
                self.combine(object_list, coordinates, radius, force, mass)
        elif distance < (radius + self.radius):
            if (force[0]+self.x_force)+(force[1]+self.y_force) > (self.mass+mass)/10000:
                for p, i in enumerate(object_list):
                    if i.get_classification() == self.get_classification() or i.get_classification() == name:
                        if "asteroid" in i.get_classification():
                            if not i.mass / 3 > mass:
                                if radius >= 3:
                                    destroyed.append(i)
                                    object_list.pop(p)
                                else:
                                    object_list.pop(p)
            else:
                for i in object_list:
                    if i.get_classification() == name:
                        i.x_force = self.x_force
                        i.y_force = self.y_force
                        self.x_force = force[0]
                        self.y_force = force[1]
        self.new_asteroid_collision(destroyed, object_list, force)

    # when two objects are inside each other they combine forming a larger object
    def combine(self, object_list, coordinates, radius, force, mass):
        x = (coordinates[0] + self.position_x) / 2
        y = (coordinates[1] + self.position_y) / 2
        radius = math.pow((3*(mass+self.mass))/(self.density*4*math.pi), 1/3)
        asteroid = Asteroid(self.screen, 100, radius, x, y, "asteroid", self.zoom)
        asteroid.set_x_force((self.x_force+force[0])/2)
        asteroid.set_y_force((self.y_force+force[1])/2)
        object_list.append(asteroid)

    # creates new smaller asteroids when to asteroids collide
    def new_asteroid_collision(self, destroyed, object_list, force):
        for i in destroyed:
            number = random.randint(1, 4)
            index = 0
            for c in range(number):
                radius = random.randint(2, 4)
                ratio = i.mass/((4/3) * math.pi * math.pow(radius, 3) * 100)
                angle = random.uniform(0, 2 * math.pi)
                x = i.get_pos_x() + random.randint(0, 5)
                y = i.get_pos_y() + random.randint(0, 5)
                asteroid = Asteroid(self.screen, 100, radius, x, y, i.get_classification()+"small"+str(index), self.zoom)
                object_list.append(asteroid)
                asteroid.set_x_force((force[0]*ratio*math.cos(angle)) / number)
                asteroid.set_y_force((force[1]*ratio*math.sin(angle)) / number)
                index += 1

    # Is used by draw lines to calculate future positions
    def calculate_future_force(self, object_mass, coordinates, position):
        direction = math.atan2(coordinates[1] - position[1], coordinates[0] - position[0])
        distance = math.sqrt(
            math.pow(position[0] - coordinates[0], 2) + math.pow(position[1] - coordinates[1], 2))
        force = (self.mass * object_mass) / math.pow(distance, 2) / 10000
        x_force = (math.cos(direction)) * force/self.mass
        y_force = (math.sin(direction)) * force/self.mass

        return x_force, y_force

    # Goes through all the forces felt by a specific object
    # and sums them all together
    def calculate_total_force(self, force_list):
        x_force = 0
        y_force = 0
        for i in force_list:
            x_force += i[0]
            y_force += i[1]
        return x_force, y_force

    # Scales the force felt during one tick and adds it
    # to the objects total force
    def add_total_force(self, force):
        self.x_force += force[0] / self.mass
        self.y_force += force[1] / self.mass

    # moves the object based on total force
    def add_new_position(self):
        self.position_x += self.x_force
        self.position_y += self.y_force

    def calculate_new_position(self, position, force):
        position_x = force[0] + position[0]
        position_y = force[1] + position[1]
        return position_x, position_y


