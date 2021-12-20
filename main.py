import pygame as pg
import math
from random import *


def draw_boid(sc, pos, angle):
    pg.draw.circle(sc, "black", pos, 5)
    xpos = pos[0] + 10*math.cos(angle), pos[1] + 10*math.sin(angle)
    pg.draw.line(sc, "black", pos, xpos, 2)


size = width, height = 1280, 720

screen = pg.display.set_mode(size)
clock = pg.time.Clock()

bxy = bx, by = 100, 200
bang = 0

while True:
    screen.fill("white")

    keys = pg.key.get_pressed()
    for event in pg.event.get():
        if event.type == pg.QUIT:
            exit()

    draw_boid(screen, bxy, bang)

    pg.display.flip()
    clock.tick()
