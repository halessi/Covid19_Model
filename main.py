'''
Authors Hugh Alessi and Georgie Nahass. Created beginning 04/19/2020, during social isolation.

Model allows for SEIRD epidemiological examination of COVID-19 kinetics. 
'''

from simulation import Simulation
import argparse

<<<<<<< HEAD
def main():
<<<<<<< HEAD
    
=======
    simulation = Simulation(number_people = NUMBER_OF_PEOPLE, 
                            step_size = STEP_SIZE,
                            infected_range = INFECTED_RANGE)
    simulation.run(number_days = 10)
=======
def main(args):
    simulation = Simulation(args)
    simulation.run(number_days = args.TD)
>>>>>>> 73c7ccd0622b49b268ba329d966b246847aec841

    args = parser.parse_args()

if __name__ == "__main__":
>>>>>>> c0ebb446a6cd108b8cb5b99aefc9718c9b0f5819
    parser = argparse.ArgumentParser()
    parser.add_argument('--E', '--exposed', help = 'initial # people exposed', type = int, default =  1)
    parser.add_argument('--I', '--infected', help = 'initial # people infected', type = int, default =  0)
    parser.add_argument('--R', '--recovered', help = 'initial # people recovered', type = int, default = 0)
    parser.add_argument('--D', '--dead', help = 'initial # people dead', type = int, default =  0)
    parser.add_argument('--TD', '--time_days', help = 'size of movement for person', type = int, default =  160)
    parser.add_argument('--TP', '--total_people', help = 'total population size', type = int, default =  10000)
    parser.add_argument('--sig', '--sigma', help = 'Rate of latent individuals becoming infected (1/latent infection period)', type = int, default =  .143)
    parser.add_argument('--gam', '--gamma', help = 'Recovery rate == 1/duration of infection = gamma', type = int, default =  .095)
    parser.add_argument('--mu', '--mu', help = ' Death rate', type = int, default =  .0034)
    parser.add_argument('--prob', '--prob_people', help = 'beta knot = probability of infection if meeting an infected person', type = int, default =  .1)
    parser.add_argument('--numb', '--numb_people', help = 'k = total number of people encountered', type = int, default =  10)

    args = parser.parse_args()
    main(args)
    