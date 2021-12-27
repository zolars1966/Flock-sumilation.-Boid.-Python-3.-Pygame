from random import *
import math


def length2D(vec):
    return math.sqrt(vec[0]*vec[0] + vec[1]*vec[1])


class Boid:
    def __init__(self, x, y, radius, width, height, i):
        self.size = self.width, self.height = width, height
        self.pos = self.x, self.y = x, y
        self.velocity = [(random()-0.5) * radius / 4, (random()-0.5) * radius / 4]
        self.acceleration = [0, 0]
        
        self.max_speed = radius / 8
        self.max_force = radius / 20
        self.perception = radius * 12

        self.index = i

    def run(self):
        self.pos = self.x, self.y = (self.x + self.velocity[0]) % self.width, (self.y + self.velocity[1]) % self.height

        self.velocity[0] += self.acceleration[0]
        self.velocity[1] += self.acceleration[1]

        if length2D(self.velocity) > self.max_speed:
            self.velocity[0] = self.velocity[0] / length2D(self.velocity) * self.max_speed
            self.velocity[1] = self.velocity[1] / length2D(self.velocity) * self.max_speed

        self.acceleration = [0, 0]

    def apply_behaviour(self, boids):
        alignment, cohesion, separation = self.rules(boids)
        
        self.acceleration[0] += alignment[0] + cohesion[0] + separation[0]
        self.acceleration[1] += alignment[1] + cohesion[1] + separation[1]

    def rules(self, boids):
        steering1 = [0, 0]
        total = 0
        avg_vec = [0, 0]

        steering2 = [0, 0]
        center_of_mass = [0, 0]

        steering3 = [0, 0]
        total1 = 0
        avg_vector1 = [0, 0]

        for i, boid in enumerate(boids):
            distance = min(abs(length2D([boid.x - self.x, boid.y - self.y])), abs(length2D([self.width - boid.x + self.x, self.height - boid.y + self.y])))
            if distance <= self.perception:
                avg_vec[0] += boid.velocity[0]
                avg_vec[1] += boid.velocity[1]
                
                center_of_mass[0] += boid.x
                center_of_mass[1] += boid.y
                total += 1

            if i != self.index and distance <= self.perception:
                diff = [self.x - boid.x, self.y - boid.y]
                diff[0] /= distance
                diff[1] /= distance
                avg_vector1[0] += diff[0]
                avg_vector1[1] += diff[1]
                total1 += 1
        
        if total > 0:
            avg_vec[0] /= total
            avg_vec[1] /= total
            avg_l = length2D(avg_vec)
            avg_vec = [avg_vec[0] / avg_l * self.max_speed, avg_vec[1] / avg_l * self.max_speed]
            steering1 = avg_vec[0] - self.velocity[0], avg_vec[1] - self.velocity[1]
            
            center_of_mass[0] /= total
            center_of_mass[1] /= total
            vec_to_come = [center_of_mass[0] - self.x, center_of_mass[1] - self.y]
            lvtc = length2D(vec_to_come)
            
            if lvtc > 0:
                vec_to_come = [vec_to_come[0] / lvtc * self.max_speed, vec_to_come[1] / lvtc * self.max_speed]
            
            steering2 = [vec_to_come[0] - self.velocity[0], vec_to_come[1] - self.velocity[1]]
            ls = length2D(steering2)
            if ls > self.max_force:
                steering2 = [steering2[0] / ls * self.max_force, steering2[1] / ls * self.max_force]

        if total1 > 0:
            avg_vector1[0] /= total1
            avg_vector1[1] /= total1

            ls = length2D(avg_vector1)
            if ls > 0:
                avg_vector1 = avg_vector1[0] / ls * self.max_speed, avg_vector1[1] / ls * self.max_speed
            
            steering3 = [avg_vector1[0] - self.velocity[0], avg_vector1[1] - self.velocity[1]]
            ls = length2D(steering3)
            if ls > self.max_force / 1.025:
                steering3 = steering3[0] / ls * self.max_force / 1.025, steering3[1] / ls * self.max_force / 1.025

        return steering1, steering2, steering3
