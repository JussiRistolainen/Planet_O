import math
import pygame
from equations import Equations
import numpy


class Planet(Equations):

    def __init__(self, screen, density, direction, angle, radius, x_axis, y_axis, sun, classification, position_x, position_y, zoom):
        super(Planet, self).__init__(screen, radius, density, classification, position_x, position_y, zoom)
        self.x_axis = x_axis
        self.y_axis = y_axis
        self.angle = angle
        self.direction = direction
        self.sun = sun
        self.major, self.minor = self.calculate_major_and_minor()
        self.distance_from_center = self.calculate_distance_from_center()
        self.eccentricity = self.calculate_eccentricity()
        self.center = self.calculate_center()
        self.area = self.calculate_area()
        self.sector_area = 50

    # defines what are the major and minor axises
    def calculate_major_and_minor(self):
        if self.x_axis >= self.y_axis:
            major = self.x_axis
            minor = self.y_axis
            return major, minor
        elif self.y_axis > self.x_axis:
            major = self.y_axis
            minor = self.x_axis
            return major, minor

    def calculate_distance_from_center(self):
        return math.sqrt(math.pow(self.major, 2) - math.pow(self.minor, 2))

    # calculates the ellipses center as it is not defined when the object is created
    def calculate_center(self):
        if self.x_axis >= self.y_axis:
            return [(self.sun.get_pos_x() + self.distance_from_center * math.cos(self.direction)), (self.sun.get_pos_y() + self.distance_from_center * math.sin(self.direction))]

        elif self.y_axis > self.x_axis:
            return [(self.sun.get_pos_x() + self.distance_from_center * math.sin(self.direction)), (self.sun.get_pos_y() + self.distance_from_center * math.cos(self.direction))]

    # calculates the ellipses eccentricity
    def calculate_eccentricity(self):
        return self.distance_from_center/self.major

    # calculates ellipse area
    def calculate_area(self):
        area = math.pi * self.x_axis * self.y_axis
        return area

    # calculates ellipse area from starting angle when "angle" is added
    def calculate_sector_area(self, angle):
        angle += math.pi
        e = 2 * math.atan(math.sqrt((1 - self.eccentricity) / (1 + self.eccentricity)) * math.tan((angle / 2)))
        m = e - self.eccentricity * math.sin(e)
        area = (1/2) * self.major * self.minor * m
        return area

    # iterating function that finds the angle that moves the object a certain amount.
    # Should be rewritten using newton raphson method.
    def calculate_new_angle(self):
        start_angle = self.angle + 0.0005
        new_area = 0
        while self.sector_area > new_area:
            old_area = self.calculate_sector_area(self.angle)

            new_area = self.calculate_sector_area(start_angle)

            start_angle += 0.0005

            new_area = abs(new_area - old_area)
        start_angle -= self.angle
        return start_angle

    # calculates at what angle the planet is with respect to the ellipse
    def calculate_angle_from_focal_point(self):
        self.center = self.calculate_center()
        theta = math.atan((self.position_y-self.center[1])/(self.position_x-self.center[0]))
        return theta

    # draws the ellipse center
    def draw_center(self):
        pygame.draw.circle(self.screen, self.color, [self.center[0] * self.zoom, self.center[1] * self.zoom], 1)

    # draws the ellipses two foci
    def draw_foci(self):
        if self.x_axis >= self.y_axis:
            a = (self.center[0] + self.distance_from_center * math.cos(self.direction)) * self.zoom
            b = (self.center[1] + self.distance_from_center * math.sin(self.direction)) * self.zoom
            pygame.draw.circle(self.screen, self.color, [a, b], 1)
        else:
            a = (self.center[0] + self.distance_from_center * math.sin(self.direction)) * self.zoom
            b = (self.center[1] + self.distance_from_center * math.cos(self.direction)) * self.zoom
            pygame.draw.circle(self.screen, self.color, [a, b], 1)

    # draws the ellipse
    def draw_ellipse(self):
        self.draw_rect_angle(((self.center[0]-self.x_axis) * self.zoom, (self.center[1]-self.y_axis) * self.zoom, (2*self.x_axis) * self.zoom, (2*self.y_axis) * self.zoom), - self.direction * 180 / math.pi)

    # calculates the planets new position on the ellipse
    def calculate_new_position(self):
        self.calculate_angle_from_focal_point()
        x = self.x_axis * math.cos(self.angle)
        y = self.y_axis * math.sin(self.angle)
        self.angle += self.calculate_new_angle()
        if self.angle > 2*math.pi:
            self.angle -= 2*math.pi
        x0 = x * math.cos(self.direction) - y * math.sin(self.direction) + self.center[0]
        y0 = x * math.sin(self.direction) + y * math.cos(self.direction) + self.center[1]

        self.position_y = y0
        self.position_x = x0

    # Is used to draw the ellipse
    def draw_rect_angle(self, rect, angle):
        target_rect = pygame.Rect(rect)
        shape_surf = pygame.Surface(target_rect.size, pygame.SRCALPHA)
        pygame.draw.ellipse(shape_surf, self.color, (0, 0, self.x_axis*2 *self.zoom, self.y_axis*2 * self.zoom), 1)
        rotated_surf = pygame.transform.rotate(shape_surf, angle)
        self.screen.blit(rotated_surf, rotated_surf.get_rect(center=target_rect.center))


