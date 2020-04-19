# execute main simulation script
from simulation import Simulation

STEP_SIZE = 0.1
NUMBER_OF_PEOPLE = 2500
NUMBER_OF_DAYS = 10
INFECTED_RANGE = 0.25
BETA = 0                    # magnitude of social distancing
SIGMA = 0                   # incubation rate (i.e., time to symptoms showing)
GAMMA = 0                   # recovery rate
MU = 0                      # death rate
S0 = 0                                         

def main():
    simulation = Simulation(number_people = NUMBER_OF_PEOPLE, 
                            step_size = STEP_SIZE,
                            infected_range = INFECTED_RANGE)
    simulation.run(number_days = 10)

if __name__ == "__main__":
    main()