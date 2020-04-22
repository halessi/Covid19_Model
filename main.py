'''
Authors Hugh Alessi and Georgie Nahass. Created beginning 04/19/2020, during social isolation.

Model allows for SEIRD epidemiological examination of COVID-19 kinetics. 
'''

from simulation import Simulation
import argparse

STEP_SIZE = 0.2
NUMBER_OF_PEOPLE = 22500
NUMBER_OF_DAYS = 10
INFECTED_RANGE = 1
BETA = 0                    # magnitude of social distancings
SIGMA = 0.14                # incubation rate (i.e., time to symptoms showing)
GAMMA = 0                   # recovery rate
MU = 0                      # death rate
S0 = 0                                         

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('--sz', '--step_size', help = 'size of movement for person', type = int, default =  5)

    simulation = Simulation(number_people = NUMBER_OF_PEOPLE, 
                            step_size = STEP_SIZE,
                            infected_range = INFECTED_RANGE)
    simulation.run(number_days = 10)

    args = parser.parse_args()

if __name__ == "__main__":
    main()