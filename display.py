import pygame


class Display:

    def __init__(self, screen, window_size,  object_list, zoom):
        self.screen = screen
        self.window_size = window_size
        self.object_list = object_list
        self.ground = (0, 0, 0)
        self.zoom = zoom

    def draw_world(self):
        for i in self.object_list:
            if "planet" in i.classification:
                i.calculate_new_position()
            self.draw_planet(i.color, [i.get_pos_x() * self.zoom, i.get_pos_y() * self.zoom], i.get_radius()* self.zoom)

    def draw_planet(self, color, position, radius):
        pygame.draw.circle(self.screen, color, position, radius)

    def draw_ellipse(self):
        for i in self.object_list:
            if "planet" in i.classification:
                i.draw_ellipse()
                i.draw_center()
                i.draw_foci()

    def set_screen(self, screen, engine):
        self.screen = screen
        engine.screen = screen
        for i in self.object_list:
            i.set_screen(screen)

    def set_zoom(self, zoom):
        self.zoom = zoom
        for i in self.object_list:
            i.set_zoom(zoom)

    # Draws expected course of asteroids (press v to show)
    def draw_line(self):
        for p in self.object_list:
            if "asteroid" in p.classification:
                position = [p.get_pos_x() * self.zoom, p.get_pos_y()  * self.zoom]
                x_force = p.get_x_force()
                y_force = p.get_y_force()
                name = p.get_classification()
                for c in range(10):
                    force_list = []
                    for i in self.object_list:
                        if name != i.get_classification():
                            if "planet" in i.classification or "Sun" in i.classification or "asteroid" in i.classification:
                                force_list.append(p.calculate_future_force(i.mass, [i.get_pos_x(), i.get_pos_y()], position))
                    force = p.calculate_total_force(force_list)
                    x_force += force[0]
                    y_force += force[1]
                    position = p.calculate_new_position(position, [x_force, y_force])
                    pygame.draw.circle(self.screen, [100, 0, 0], [position[0], position[1]], 1)



