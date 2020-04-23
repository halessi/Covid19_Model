import math

import numpy as np
from DSEIR import DSEIR
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
            
        self.all_people = [self.people,
                           self.infected_people,
                           self.dead_people,
                           self.recovered_people,
                           self.exposed_people]

        self.DSEIR = DSEIR(args)
        self.DSEIR_values = self.DSEIR.getDSEIR() # S E I R D, order

        self.plot = self.load_plot(number_people = args.TP)

    def load_plot(self, number_people):
        # calculate square root
        root = math.sqrt(number_people)

        self.fig = plt.figure(figsize=(10,10))
        self.ax = plt.axes(xlim = (0, root), ylim = (0, root))
        self.d, = self.ax.plot([person.coordinates[0] for person in self.people],
                               [person.coordinates[1] for person in self.people], 'bo', label = 'susceptible: {}'.format(len(self.people)), markersize = 2)
        self.i, = self.ax.plot([person.coordinates[0] for person in self.infected_people], 
                               [person.coordinates[1] for person in self.infected_people], 'ro', label = 'infected: {}'.format(len(self.infected_people)), markersize = 2)
        self.e, = self.ax.plot([person.coordinates[0] for person in self.exposed_people],
                               [person.coordinates[1] for person in self.exposed_people], 'mo', label = 'exposed: {}'.format(len(self.exposed_people)), markersize = 2)
        self.r, = self.ax.plot([person.coordinates[0] for person in self.recovered_people], 
                               [person.coordinates[1] for person in self.recovered_people], 'go', label = 'recovered: {}'.format(len(self.recovered_people)), markersize = 2)
        self.p, = self.ax.plot([person.coordinates[0] for person in self.dead_people], 
                               [person.coordinates[1] for person in self.dead_people], 'ko', label = 'dead: {}'.format(len(self.recovered_people)), markersize = 2)
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

    def update(self):
        number_new_exposed     = int(self.DSEIR_values[1][self.day] - len(self.exposed_people))
        number_new_infected    = int(self.DSEIR_values[2][self.day] - len(self.infected_people))
        number_new_recovered   = int(self.DSEIR_values[3][self.day] - len(self.recovered_people))
        number_new_dead        = int(self.DSEIR_values[4][self.day] - len(self.dead_people))
       
        self.assign_new_recovered(number = number_new_recovered)
        self.assign_new_dead(number = number_new_dead)
        self.assign_new_infection(number = number_new_infected)

    def assign_new_dead(self, number):
        for i in range(0, number):
            new_dead_person = np.random.randint(0, len(self.infected_people))
            new_dead_person = self.infected_people[new_dead_person]

            new_dead_person.infected = False
            new_dead_person.dead = True

            self.infected_people.remove(new_dead_person)
            self.dead_people.append(new_dead_person)

    def assign_new_recovered(self, number):
        for i in range(0, number):
            recoveree = np.random.randint(0, len(self.infected_people))
            recoveree = self.infected_people[recoveree]

            recoveree.infected = False
            recoveree.recovered = True

            self.infected_people.remove(recoveree)
            self.recovered_people.append(recoveree)

    def assign_new_infection(self, number):
        # randomly decide which infected person is going to infect another 
        # !this could probably be done by figuring out which infected person is closest to another, but alas

        for i in range(number):
            infector = np.random.randint(0, len(self.exposed_people))
            infector = self.exposed_people[infector]

            x_infector, y_infector = infector.coordinates[0], infector.coordinates[1]

            # find the closest healthy person to the infector
            closest_person_to_infector = self.find_closest_person(infector, type = 'SUSCEPTIBLE')

            # get em
            closest_person_to_infector.infected = True
            self.people.remove(closest_person_to_infector)
            self.infected_people.append(closest_person_to_infector)

    def find_closest_person(self, POI, type = None):
        '''
        find the closest person of a specific type to another person

        args:
            POI: the person we want to find another close to
            type: can be SUSCEPTIBLE, EXPOSED, INFECTED, RECOVERED, DEAD,

        returns:
            person object of closest person
        '''

        if type is not None:
            # i think that checking for specific type and choosing list
            # will be faster than iterating through all people and checking type, for people > 10000ish
            if type == 'SUSCEPTIBLE':
                people_of_interest = self.people
            elif type == 'INFECTED':
                people_of_interest = self.infected
            elif type == 'EXPOSED':
                people_of_interest = self.exposed
            elif type == 'DEAD':
                people_of_interest = self.dead
            elif type == 'RECOVERED':
                people_of_interest = self.recovered
            else:
                print('Error in find_closest_person: query type INVALID')
        else:
            print('Error in find_closest_person: query requested without specifying type')

        x_POI, y_POI = POI.coordinates[0], POI.coordinates[1]
        # probably a better way to do this, but l0l
        x_dif_init, y_dif_init = 10000, 10000
        chosen_person = None

        for i in range(0, len(people_of_interest)):
            x, y = people_of_interest[i].coordinates[0], people_of_interest[i].coordinates[1]
            x_dif, y_dif = abs(x_POI - x), abs(y_POI - y)   
            if (x_dif + y_dif) < (x_dif_init + y_dif_init):
                x_dif_init, y_dif_init = x_dif, y_dif
                chosen_person = people_of_interest[i]

        return chosen_person

    def animate(self, b):
        ''' 
        Create the animation. Function is CALLED by self.run()
        every step of the simulation, updating dot placement and infected
        status. 
        '''
        for person_type in self.all_people:
            for person in person_type:
                person.take_step()

        self.day += 1
        self.update()

        self.d.set_data([person.coordinates[0] for person in self.people],
                        [person.coordinates[1] for person in self.people])   

        self.i.set_data([person.coordinates[0] for person in self.infected_people],
                        [person.coordinates[1] for person in self.infected_people])

        self.e.set_data([person.coordinates[0] for person in self.exposed_people],
                        [person.coordinates[1] for person in self.exposed_people]) 

        self.r.set_data([person.coordinates[0] for person in self.recovered_people],
                        [person.coordinates[1] for person in self.recovered_people]) 

        self.p.set_data([person.coordinates[0] for person in self.dead_people],
                        [person.coordinates[1] for person in self.dead_people]) 

        legend = plt.legend(['healthy: {}'.format(len(self.people)), 
                             'infected: {}'.format(len(self.infected_people)),
                             'exposed: {}'.format(len(self.exposed_people)),
                             'recovered: {}'.format(len(self.recovered_people)),
                             'dead: {}'.format(len(self.dead_people))],
                            #'day: {}'.format(self.day)], 
                            loc = 'upper left')

        return self.d, self.i, legend

    def run(self, number_days = 5):
        anim = animation.FuncAnimation(self.fig, self.animate, interval = 10)
        plt.show()

    '''old function for random'''
    # def check_infections(self):
    #     '''
    #     For each infected person, check whether they've come into contact with
    #     a healthy individual by comparing coordinates. 
    #     '''
    #     for infected_person in self.infected_people:
    #         x, y = infected_person.coordinates[0], infected_person.coordinates[1]
    #         x_high, x_low = x + self.infected_range, x - self.infected_range
    #         y_high, y_low = y + self.infected_range, y - self.infected_range

    #         for healthy_person in self.people:
    #              if (x_high > healthy_person.coordinates[0] > x_low) and (y_high > healthy_person.coordinates[1] > y_low):
    #                     healthy_person.infected = True
    #                     self.people.remove(healthy_person)
    #                     self.infected_people.append(healthy_person)
