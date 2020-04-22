import math

import numpy as np
from matplotlib import animation
from matplotlib import pyplot as plt
from person import Person
from utils import *

class Simulation():
    '''
    Runs the simulation and handles updating visuals over time. 
    '''

    def __init__(self, args):
        self.infected_people, self.dead_people, self.exposed_people, self.recovered_people = [], [], [], []
        self.day = 0

        self.people = self.load_people(number_people = args.TP, 
                                       number_infected = args.I,
                                       number_exposed = args.E,
                                       )
        self.plot = self.load_plot(number_people = args.TP)

    def load_plot(self, number_people):
        # calculate square root
        root = math.sqrt(number_people)

        self.fig = plt.figure(figsize=(10,10))
        self.ax = plt.axes(xlim = (0, root), ylim = (0, root))
        self.d, = self.ax.plot([person.coordinates[0] for person in self.people],
                               [person.coordinates[1] for person in self.people], 'bo', label = 'healthy: {}'.format(len(self.people)), markersize = 1)
        self.i, = self.ax.plot([person.coordinates[0] for person in self.infected_people], 
                               [person.coordinates[1] for person in self.infected_people], 'ro', label = 'infected: {}'.format(len(self.infected_people)), markersize = 1)
        self.e, = self.ax.plot([person.coordinates[0] for person in self.exposed_people],
                               [person.coordinates[1] for person in self.exposed_people], 'oo')
        plt.legend(loc = 'upper left')
        return 

    def load_people(self, number_people, number_infected, number_exposed):
        '''Create person objects up to number of people. 

        args:
            number_people: the number of people in the simulation
            step_size: for each step in the simulation, degree of individual movement

        returns:
            list containing people
        '''

        root = int(math.sqrt(number_people))

        if is_square(number_people):
            print('Number of people in simulation: {}.'.format(number_people))
        else:
            print('Number of people in simulation must be a perfect square. {} is not, try again.'.format(number_people))
            exit()

        people = []
        x,y = 1, 1
        for i in range(root):
            people.append(Person(x, y))
            for i in range(root - 1):
                y += 1
                people.append(Person(x, y))
            x += 1
            y = 1

        # probably want to concatenate this into one loop, kinda unfortunate as is
        for i in range(0, number_exposed):
            person = people[np.random.randint(0, number_people)]
            person.exposed = True
            people.remove(person)
            self.exposed_people.append(person)

        for i in range(0, number_infected):
            person = people[np.random.randint(0, number_people)]
            person.exposed = True
            people.remove(person)
            self.infected_people.append(person)

        return people
    
    def check_infections(self):
        '''
        For each infected person, check whether they've come into contact with
        a healthy individual by comparing coordinates. 
        '''
        for infected_person in self.infected_people:
            x, y = infected_person.coordinates[0], infected_person.coordinates[1]
            x_high, x_low = x + self.infected_range, x - self.infected_range
            y_high, y_low = y + self.infected_range, y - self.infected_range

            for healthy_person in self.people:
                 if (x_high > healthy_person.coordinates[0] > x_low) and (y_high > healthy_person.coordinates[1] > y_low):
                        healthy_person.infected = True
                        self.people.remove(healthy_person)
                        self.infected_people.append(healthy_person)

    def animate(self, b):
        ''' 
        Create the animation. Function is CALLED by self.run()
        every step of the simulation, updating dot placement and infected
        status. 
        '''
        for person in self.people:
            person.take_step()

        for person in self.infected_people:
            person.take_step(step_size = 0.1)

        self.check_infections()

        self.d.set_data([person.coordinates[0] for person in self.people],
                        [person.coordinates[1] for person in self.people])   

        self.i.set_data([person.coordinates[0] for person in self.infected_people],
                        [person.coordinates[1] for person in self.infected_people])

        legend = plt.legend(['healthy: {}'.format(len(self.people)), 
                            'infected: {}'.format(len(self.infected_people))],
                            #'day: {}'.format(self.day)], 
                            loc = 'upper left')

        return self.d, self.i, legend

    def run(self, number_days = 5):
        anim = animation.FuncAnimation(self.fig, self.animate, interval = 1)
        plt.show()
