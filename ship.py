from equations import Equations
from asteroid import Asteroid
import math


class Ship(Equations):

    def __init__(self, screen, density, radius, position_x, position_y, classification, zoom):
        super(Ship, self).__init__(screen, radius, density, classification, position_x, position_y, zoom)
        self.fuel = 100
        self.index_bullet = 0

    # moves the object left
    def move_left(self):
        if self.fuel > 0:
            self.x_force -= 0.5
            self.fuel -= 1

    # moves the object right
    def move_right(self):
        if self.fuel > 0:
            self.x_force += 0.5
            self.fuel -= 1

    # moves the object up
    def move_up(self):
        if self.fuel > 0:
            self.y_force -= 0.5
            self.fuel -= 1

    # moves the object down
    def move_down(self):
        if self.fuel > 0:
            self.y_force += 0.5
            self.fuel -= 1

    # shoots an asteroid object in the direction of the mouse with a set velocity
    def shoot(self, object_list, coordinates):
        direction = math.atan2(coordinates[1] - self.position_y,  coordinates[0] - self.position_x)
        self.index_bullet += 1
        radius = 1
        density = 100
        mass = (4/3) * math.pow(radius, 3) * density
        A = Asteroid(self.screen, density, radius, (self.position_x + self.radius * 3 * math.cos(direction)), (self.position_y + self.radius* 3 * math.sin(direction)), "asteroidBullet"+ str(self.index_bullet), self.zoom)
        A.set_x_force(1000 * math.cos(direction)/ mass)
        A.set_y_force(1000 * math.sin(direction)/ mass)
        self.x_force -= (1000 * math.cos(direction)/ self.mass)
        self.y_force -= (1000 * math.sin(direction) / self.mass)
        object_list.append(A)

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








