[![Back](https://user-images.githubusercontent.com/70763346/205440694-aa92ef86-80c0-4935-855b-34f0fdddd160.png)](https://zolars1966.github.io/)

# Boid
# En

## Info
Flying Boids

Result on youtube:
[![Watch the video](https://img.youtube.com/vi/D3F6j38yzjY/maxresdefault.jpg)](https://www.youtube.com/watch?v=D3F6j38yzjY)

Minimum requirentments:
* Python 3.4.x
* Pygame 2.x
* Numpy
* Math

Language: ![https://img.shields.io/badge/Python-3.10-red](https://img.shields.io/badge/Python-3.10-red)

# Code explaining

## Length2D
```length2D``` is frequently used function, it returns length of vector, that you sent

Python realization
``` Python
def length2D(vec):
    return math.sqrt(vec[0]*vec[0] + vec[1]*vec[1])
```

## Class Flock

Method ```run``` calls in main cycle in ```main``` file.

Python realization
``` Python
class Flock:
    def __init__(self, b_num, radius, width, height):
        self.boids = [Boid(randint(0, width-1), randint(0, height-1), radius, width, height, i) for i in range(b_num)]

    def run(self):
        for boid in self.boids:
            boid.run()
            boid.apply_behaviour(self.boids)
```

## Class Boid

Parameter ```i```, means Boid index in ```boids``` list.

Python realization
``` Python
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
```

## Boid movement

Python realization
``` Python
def run(self, boids):
        self.pos = self.x, self.y = (self.x + self.velocity[0]) % self.width, (self.y + self.velocity[1]) % self.height

        self.velocity[0] += self.acceleration[0]
        self.velocity[1] += self.acceleration[1]

        self.velocity[0] = math.cos(angle)
        self.velocity[1] = math.sin(angle)

        if length2D(self.velocity) > self.max_speed:
            self.velocity[0] = self.velocity[0] / length2D(self.velocity) * self.max_speed
            self.velocity[1] = self.velocity[1] / length2D(self.velocity) * self.max_speed

        self.acceleration = [0, 0]
```

## Rules

![https://www.researchgate.net/profile/Noury-Bouraqadi/publication/228771083/figure/fig4/AS:668681436688392@1536437486279/Flocking-Relies-on-3-Rules-for-Steering-Individual-Boids.png](https://www.researchgate.net/profile/Noury-Bouraqadi/publication/228771083/figure/fig4/AS:668681436688392@1536437486279/Flocking-Relies-on-3-Rules-for-Steering-Individual-Boids.png "Visualization")

### Apply rules to Boid

Python realization
``` Python
def apply_behaviour(self, boids):
        alignment = self.align(boids)
        cohesion = self.cohesion(boids)
        separation = self.separation(boids)
        
        self.acceleration[0] += alignment[0] + cohesion[0] + separation[0]
        self.acceleration[1] += alignment[1] + cohesion[1] + separation[1]
```

### Separation

Each boid also tries to avoid running into the other boids. If it gets too close to another boid it will steer away from it.

Python realiazation
``` Python
def separation(self, boids):
        steering = [0, 0]
        total = 0
        avg_vector = [0, 0]

        for i, boid in enumerate(boids):
            distance = min(abs(length2D([boid.x - self.x, boid.y - self.y])), abs(length2D([1280 - boid.x + self.x, 720 - boid.y + self.y])))
            if i != self.index and distance < self.perception:
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
```

### Cohesion

Each boid flies towards the the other boids. But they don't just immediately fly directly at each other. They gradually steer towards each other at a rate that you can adjust with the "coherence" slider.

Python realization
``` Python
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
```

### Alignment

Finally, each boid tries to match the vector (speed and direction) of the other boids around it.

Python realization
``` Python
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
```


[![Back](https://user-images.githubusercontent.com/70763346/205440694-aa92ef86-80c0-4935-855b-34f0fdddd160.png)](https://zolars1966.github.io/)
