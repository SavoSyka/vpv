import pygame as pg
from pygame.draw import *
from random import randint
from math import sin, cos
pg.init()

FPS = 100
screen = pg.display.set_mode((1200, 900))
screen.fill((50, 50, 50))

RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]

x_center = 600
y_center = 450
g = 9.8
m = 5
R = 300
A = 5
w = 300
t = 0
dt = 0.01
theta = 0.2
dtheta = 0
size = 15

x = R * sin(theta) + 600
y = A * sin(w*t) - R * cos(theta) + 300

pg.display.update()
clock = pg.time.Clock()
finished = False

while not finished:
    pg.display.update()
    screen.fill((50, 50, 50))
    clock.tick(FPS)

    ddtheta = (-A * (w ** 2) * sin(w*t) + g) * sin(theta) / R
    dtheta += ddtheta * dt
    theta += dtheta * dt
    x = R * sin(theta) + x_center
    y = A * sin(w * t) - R * cos(theta) + y_center
    circle(screen, (255, 255, 255), (x_center, y_center+A*sin(w*t)), size)
    circle(screen, (199, 199, 0), (x, y), size)

    line(screen, (255, 255, 255), (x_center, y_center), (x, y))
    t += dt
    for event in pg.event.get():
        if event.type == pg.QUIT:
            finished = True

pg.quit()