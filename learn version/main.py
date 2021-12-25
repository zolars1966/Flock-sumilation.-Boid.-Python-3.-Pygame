from random import *
from flock import Flock
import pygame as pg
import math
import sys

radian = math.pi/180
TICK_RATE = 32
size = width, height = 1280, 720


def length2D(vec):
    return math.sqrt(vec[0]*vec[0] + vec[1]*vec[1])


def draw_boids(sc, boids):
    for boid in boids:
        pg.draw.circle(sc, "black", boid.pos, 5)
        lv = length2D(boid.velocity)
        xpos = boid.pos[0] + 10*boid.velocity[0]/lv, boid.pos[1] + 10*boid.velocity[1]/lv
        pg.draw.line(sc, "black", boid.pos, xpos, 2)


if __name__ == "__main__":
    screen = pg.display.set_mode(size, vsync=1)
    clock = pg.time.Clock()

    flock = Flock(30)

    upd_ticks = pg.time.get_ticks()

    while True:
        screen.fill("white")

        keys = pg.key.get_pressed()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                sys.exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_u:
                    TICK_RATE -= 1
                    upd_ticks = pg.time.get_ticks()
                if event.key == pg.K_i:
                    TICK_RATE += 1
                    upd_ticks = pg.time.get_ticks()

        draw_boids(screen, flock.boids)
        
        if True:#pg.time.get_ticks() - upd_ticks >= (1000 / TICK_RATE):
            flock.run((pg.time.get_ticks() - upd_ticks)/1000)
            flock.run((pg.time.get_ticks() - upd_ticks)/1000)
            upd_ticks = pg.time.get_ticks()

        pg.display.set_caption("$~Boids ~fps: " + str(round(clock.get_fps(), 2)) + " ~tickrate: " + str(TICK_RATE))

        pg.display.flip()
        clock.tick()
