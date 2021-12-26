from random import *
from flock import Flock
import pygame as pg
import math
import sys

TICK_RATE = 128
FPS = 32
size = width, height = 128*2, 72*2
radius = 5
num = 32


def length2D(vec):
    return math.sqrt(vec[0]*vec[0] + vec[1]*vec[1])


def draw_boids(sc, boids):
    for boid in boids:
        pg.draw.circle(sc, "black", boid.pos, radius)
        lv = length2D(boid.velocity)
        # xpos = boid.pos + boid.velocity / lv * 10
        xpos = boid.pos[0] + radius*2*boid.velocity[0]/lv, boid.pos[1] + radius*2*boid.velocity[1]/lv
        pg.draw.line(sc, "black", boid.pos, xpos, int(radius/2.5))


if __name__ == "__main__":
    screen = pg.display.set_mode(size, vsync=1)
    clock = pg.time.Clock()

    flock = Flock(num, radius, width, height)

    upd_ticks = pg.time.get_ticks()

    while True:
        screen.fill("white")

        keys = pg.key.get_pressed()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                sys.exit()

        draw_boids(screen, flock.boids)

        if TICK_RATE != 0:
            ticks = pg.time.get_ticks()
            if ticks - upd_ticks >= (1000 / TICK_RATE):
                flock.run()
                flock.run()
                flock.run()
                flock.run()
                upd_ticks = ticks - (ticks - upd_ticks) % (1000 / TICK_RATE)
        else:
            flock.run()
            flock.run()
            flock.run()
            flock.run()

        pg.display.set_caption("$~Boids ~fps: " + str(round(clock.get_fps(), 2)) + " ~tickrate: " + str(TICK_RATE))

        pg.display.flip()
        clock.tick(FPS)
