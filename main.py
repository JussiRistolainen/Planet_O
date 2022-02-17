import pygame
from display import Display
from world_creator import World
from engine import Engine


def main():

    # creates window
    window_size = (1480, 920)
    window = pygame.display.set_mode(window_size)
    object_list = []
    zoom = 0.5
    # Surface we draw all our planets on
    screen = pygame.Surface((window_size[0], window_size[1]))
    # Objects
    display = Display(screen, window_size, object_list, zoom)
    engine = Engine(screen, object_list)
    world = World(screen, object_list, zoom)

    running = True
    fps = 30
    clock = pygame.time.Clock()
    time = pygame.USEREVENT + 1
    pygame.time.set_timer(time, 100)

    # creating drawable objects
    world.create_sun(1, [500, 500], 200)
    world.create_sun(1, [1000, 1000], 200)
    world.create_planet_with_moon(3, 2, "Sun0")
    world.create_planet_with_moon(3, 2, "Sun1")
    world.create_asteroid(5)
    ship = world.create_ship([100, 100])

    ellipses = False
    lines = False
    follow = False
    pos = [0, 0]
    # The core game engine
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == time:
                screen = pygame.Surface((int(window_size[0]) / 0.5, int(window_size[1]) / 0.5))
                display.set_screen(screen, engine)
                display.set_zoom(zoom)
                screen.fill((0, 0, 0))
                window.blit(screen, (0, 0))
                display.draw_world()
                engine.calculate_force()
            if event.type == pygame.KEYDOWN:
                mouse = pygame.mouse.get_pos()
                if event.key == pygame.K_c:
                    ellipses = not ellipses
                if event.key == pygame.K_v:
                    lines = not lines
                if event.key == pygame.K_o:
                    if zoom < 2:
                        zoom += 0.2
                if event.key == pygame.K_l:
                    if zoom > 0.5:
                        zoom -= 0.2
                if event.key == pygame.K_w:
                    ship.move_up()
                if event.key == pygame.K_d:
                    ship.move_right()
                if event.key == pygame.K_a:
                    ship.move_left()
                if event.key == pygame.K_s:
                    ship.move_down()
                if event.key == pygame.K_i:
                    ship.shoot(object_list, [(-pos[0] + mouse[0])/zoom, (-pos[1] + mouse[1])/zoom])
                if event.key == pygame.K_SPACE:
                    pos[0] = -ship.position_x + window_size[0] / zoom / 2
                    pos[1] = -ship.position_y + window_size[1] / zoom / 2
                if event.key == pygame.K_f:
                    follow = not follow
            # enables screen movement
            mouse = pygame.mouse.get_pos()
            if mouse[0] > window_size[0] / 4 * 3:
                pos[0] -= (mouse[0] - (window_size[0] / 4 * 3))/10
            if mouse[0] < window_size[0] / 4:
                pos[0] += ((window_size[0] / 4) - mouse[0])/10
            if mouse[1] > (window_size[1] / 4 * 3):
                pos[1] -= (mouse[1] - (window_size[1] / 4 * 3)) / 10
            if mouse[1] < (window_size[1] / 4):
                pos[1] += ((window_size[1] / 4) - mouse[1]) / 10
            if ellipses:
                display.draw_ellipse()
            if lines:
                display.draw_line()
            if follow:
                pos[0] = (-ship.position_x * zoom) + (window_size[0]) / 2
                pos[1] = (-ship.position_y * zoom) + (window_size[1]) / 2
            window.blit(screen, pos)
            pygame.display.update()

        clock.tick(fps)


if __name__ == "__main__":
    main()
