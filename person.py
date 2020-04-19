import numpy as np
import math

class Person():

    def __init__(self, x, y, step_size):
        self.infected = False
        self.step_size = step_size
        self.age = np.random.randint(low = 1, high = 100)
        self.coordinates = (x, y)

    def take_step(self, step_size = -1):
        if step_size == -1:
            step_size = self.step_size
        degree_direction = np.random.randint(low= 0, high = 360)
        radian_direction = (degree_direction * math.pi) / 180
        self.coordinates = (self.coordinates[0] + (step_size * math.cos(radian_direction)),
                            self.coordinates[1] + (step_size * math.sin(radian_direction)))
