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
                           self.exposed_people
                           ]

        self.DSEIR = DSEIR(args)
        self.DSEIR_values = list(self.DSEIR.getDSEIR()) # S E I R D, order
        self.DSEIR_values.append([i for i in range(0, len(self.DSEIR_values[0]))])
        self.plot = self.load_plot(number_people = args.TP)

    def load_plot(self, number_people):
        # calculate square root
        root = math.sqrt(number_people)

        self.fig, self.axs = plt.subplots(2, figsize = (10,10))
        self.axs[0].set_xlim(0, len(self.DSEIR_values[-1]))
        self.axs[0].set_ylim(0, number_people)

        self.d, = self.axs[1].plot([person.coordinates[0] for person in self.people],
                               [person.coordinates[1] for person in self.people], 'bo', label = 'susceptible: {}'.format(len(self.people)), markersize = 2)
        self.i, = self.axs[1].plot([person.coordinates[0] for person in self.infected_people], 
                               [person.coordinates[1] for person in self.infected_people], 'ro', label = 'infected: {}'.format(len(self.infected_people)), markersize = 2)
        self.e, = self.axs[1].plot([person.coordinates[0] for person in self.exposed_people],
                               [person.coordinates[1] for person in self.exposed_people], 'mo', label = 'exposed: {}'.format(len(self.exposed_people)), markersize = 2)
        self.r, = self.axs[1].plot([person.coordinates[0] for person in self.recovered_people], 
                               [person.coordinates[1] for person in self.recovered_people], 'go', label = 'recovered: {}'.format(len(self.recovered_people)), markersize = 2)
        self.p, = self.axs[1].plot([person.coordinates[0] for person in self.dead_people], 
                               [person.coordinates[1] for person in self.dead_people], 'ko', label = 'dead: {}'.format(len(self.recovered_people)), markersize = 2)

        self.lineS, = self.axs[0].plot((0, 0), 'b')
        self.lineE, = self.axs[0].plot((0, 0), 'r')
        self.lineI, = self.axs[0].plot((0, 0), 'm')
        self.lineR, = self.axs[0].plot((0, 0), 'g')
        self.lineD, = self.axs[0].plot((0, 0), 'k')

        #self.axs[1].legend(loc = 'upper left')
        self.axs[0].legend(bbox_to_anchor = (1.1, 1.1))
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
        try:
            number_new_exposed     = int(self.DSEIR_values[1][self.day] - len(self.exposed_people))
            number_new_infected    = int(self.DSEIR_values[2][self.day] - len(self.infected_people))
            number_new_recovered   = int(self.DSEIR_values[3][self.day] - len(self.recovered_people))
            number_new_dead        = int(self.DSEIR_values[4][self.day] - len(self.dead_people))
        except:
            return

        self.assign_new_infected(number = number_new_infected)
        self.assign_new_exposed(number = number_new_exposed)
        self.assign_new_dead(number = number_new_dead)
        self.assign_new_recovered(number = number_new_recovered)

    def assign_new_exposed(self, number):
        ''' 
        select a random person to become infected based upon
        proximity to an infected person
        '''

        for i in range(0, number):
            try:
                # this will fail the first few loops, as there is no infected person...sometimes
                infector = self.infected_people[np.random.randint(0, len(self.infected_people))]
            except ValueError:
                print('assign_new_exposed(): no infected person from which to assign exposed, drawing from exposed')
                #! draw from exposed in that case !?
                infector = self.exposed_people[np.random.randint(0, len(self.exposed_people))]
            x_infector, y_infector = infector.coordinates[0], infector.coordinates[1]

            # find the closest healthy person to the infector
            closest_person_to_infector = self.find_closest_person(infector, type = 'SUSCEPTIBLE')

            self.people.remove(closest_person_to_infector)
            self.exposed_people.append(closest_person_to_infector)

    def assign_new_dead(self, number):
        for i in range(0, number):
            new_dead_person = self.infected_people[np.random.randint(0, len(self.infected_people))]

            self.infected_people.remove(new_dead_person)
            self.dead_people.append(new_dead_person)

    def assign_new_recovered(self, number):
        for i in range(0, number):
            recoveree = self.infected_people[np.random.randint(0, len(self.infected_people))]

            self.infected_people.remove(recoveree)
            self.recovered_people.append(recoveree)

    def assign_new_infected(self, number):
        for i in range(0, number):
            # select new infected person from those who have been exposed
            try:
                # at the end of the simulation, sometimes a person becomes infected while there are 0 exposed
                # assign it from healthy if this happens
                new_infected_person = self.exposed_people[np.random.randint(0, len(self.exposed_people))]
                self.exposed_people.remove(new_infected_person)
                self.infected_people.append(new_infected_person)
            except ValueError:
                print('assign_new_infected(): no exposed people from which to assign infection, drawing from healthy ')
                new_infected_person = self.people[np.random.randint(0, len(self.people))]
                self.people.remove(new_infected_person)
                self.infected_people.append(new_infected_person)

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
                people_of_interest = self.infected_people
            elif type == 'EXPOSED':
                people_of_interest = self.exposed_people
            elif type == 'DEAD':
                people_of_interest = self.dead_people
            elif type == 'RECOVERED':
                people_of_interest = self.recovered_people
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

        # update dots
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

        # update lines
        self.lineS.set_data(self.DSEIR_values[-1][0:self.day], self.DSEIR_values[0][0:self.day])
        self.lineE.set_data(self.DSEIR_values[-1][0:self.day], self.DSEIR_values[1][0:self.day])
        self.lineI.set_data(self.DSEIR_values[-1][0:self.day], self.DSEIR_values[2][0:self.day])
        self.lineR.set_data(self.DSEIR_values[-1][0:self.day], self.DSEIR_values[3][0:self.day])
        self.lineD.set_data(self.DSEIR_values[-1][0:self.day], self.DSEIR_values[4][0:self.day])

        self.axs[0].legend(['healthy: {}'.format(len(self.people)), 
                             'infected: {}'.format(len(self.infected_people)),
                             'exposed: {}'.format(len(self.exposed_people)),
                             'recovered: {}'.format(len(self.recovered_people)),
                             'dead: {}'.format(len(self.dead_people))],
                            #'day: {}'.format(self.day)], 
                            #bbox_to_anchor = (1, 1),
                             loc = 'upper left')

        return self.d, self.i, #legend

    def run(self, number_days = 5):
        anim = animation.FuncAnimation(self.fig, self.animate, interval = 50)
        #plt.show()
        anim.save('test.gif', writer = 'imagemagick', fps = 5)
        