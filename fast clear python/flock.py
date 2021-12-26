from random import *
from boid import Boid
import numpy as np


class Flock:
    def __init__(self, b_num, radius, width, height):
        self.boids = [Boid(randint(0, 1279), randint(0, 719), radius, width, height) for _ in range(b_num)]

    def run(self):
        for boid in self.boids:
            boid.run(self.boids)
            boid.apply_behaviour(self.boids)
