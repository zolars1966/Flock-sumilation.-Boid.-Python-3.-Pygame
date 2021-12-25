from random import *
import math

"""

#@!#@!#@! make from 3 cycles, one cycle !@#!@#!@#

"""


def length2D(vec):
    return math.sqrt(vec[0]*vec[0] + vec[1]*vec[1])


class Boid:
    def __init__(self, x, y):
        self.pos = self.x, self.y = x, y
        self.velocity = [(random()-0.5) * 5, (random()-0.5) * 5]
        self.acceleration = [0, 0]
        
        self.max_speed = 2
        self.max_force = 0.1
        self.perception = 30

    def run(self, time, boids):
        self.pos = self.x, self.y = (self.x + self.velocity[0]) % 1280, (self.y + self.velocity[1]) % 720

        self.velocity[0] += self.acceleration[0]
        self.velocity[1] += self.acceleration[1]

        if length2D(self.velocity) > self.max_speed:
            self.velocity[0] = self.velocity[0] / length2D(self.velocity) * self.max_speed
            self.velocity[1] = self.velocity[1] / length2D(self.velocity) * self.max_speed

        self.acceleration = [0, 0]

    def apply_behaviour(self, boids):
        alignment = self.align(boids)
        cohesion = self.cohesion(boids)
        separation = self.separation(boids)
        
        self.acceleration[0] += alignment[0] + cohesion[0] + separation[0]
        self.acceleration[1] += alignment[1] + cohesion[1] + separation[1]

    def separation(self, boids):
        steering = [0, 0]
        total = 0
        avg_vector = [0, 0]

        for boid in boids:
            distance = min(abs(length2D([boid.x - self.x, boid.y - self.y])), abs(length2D([1280 - boid.x + self.x, 720 - boid.y + self.y])))
            if self.pos != boid.pos and distance < self.perception:
                diff = [self.x - boid.x, self.y - boid.y]
                diff[0] /= distance
                diff[1] /= distance
                avg_vector[0] += diff[0]
                avg_vector[1] += diff[1]
                total += 1
        
        if total > 0:
            avg_vector[0] /= total
            avg_vector[1] /= total

            ls = length2D(avg_vector)
            if ls > 0:
                avg_vector = avg_vector[0] / ls * self.max_speed, avg_vector[1] / ls * self.max_speed
            
            steering = [avg_vector[0] - self.velocity[0], avg_vector[1] - self.velocity[1]]
            if ls > self.max_force / 5:
                steering = steering[0] / ls * self.max_force, steering[1] / ls * self.max_force / 5

        return steering

    def cohesion(self, boids):
        steering = [0, 0]
        total = 0
        center_of_mass = [0, 0]

        for boid in boids:
            distance = min(abs(length2D([boid.x - self.x, boid.y - self.y])), abs(length2D([1280 - boid.x + self.x, 720 - boid.y + self.y])))
            if distance < self.perception:
                center_of_mass[0] += boid.x
                center_of_mass[1] += boid.y
                total += 1
        
        if total > 0:
            center_of_mass[0] /= total
            center_of_mass[1] /= total
            vec_to_come = [center_of_mass[0] - self.x, center_of_mass[1] - self.y]
            lvtc = length2D(vec_to_come)
            
            if lvtc > 0:
                vec_to_come = [vec_to_come[0] / lvtc * self.max_speed, vec_to_come[1] / lvtc * self.max_speed]
            
            steering = [vec_to_come[0] - self.velocity[0], vec_to_come[1] - self.velocity[1]]
            ls = length2D(steering)
            if ls > self.max_force:
                steering = [steering[0] / ls * self.max_force, steering[1] / ls * self.max_force]

        return steering

    def align(self, boids):
        steering = [0, 0]
        total = 0
        avg_vec = [0, 0]
        
        for boid in boids:
            distance = min(abs(length2D([boid.x - self.x, boid.y - self.y])), abs(length2D([1280 - boid.x + self.x, 720 - boid.y + self.y])))
            if distance < self.perception:
                avg_vec[0] += boid.velocity[0]
                avg_vec[1] += boid.velocity[1]
                total += 1
        
        if total > 0:
            avg_vec[0] /= total
            avg_vec[1] /= total
            avg_l = length2D(avg_vec)
            avg_vec = [avg_vec[0] / avg_l * self.max_speed, avg_vec[1] / avg_l * self.max_speed]
            steering = avg_vec[0] - self.velocity[0], avg_vec[1] - self.velocity[1]

        return steering
