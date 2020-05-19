import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

class DSEIR():
    ###  SIMULATION SETUP ###
    def __init__(self, args):
        '''Begins math portion of simulation

        args:
            E: Initial number of exposed people
            I: Initial number infected people 
            R: Initial number recovered people
            D: Initial number dead people
            time_days: Length of simulation in days
            total_people: Total population size
            sigma: Rate of latent individuals becoming infected
            gamma: Recovery or mortality rate == 1 / duration of infection = gamma
            mu: Death rate
            prob_Meeting_New_Person: beta knot= probability of infection if meeting an infected person
            number_People_Encountered:
        '''
        self.E = args.E                          
        self.I = args.I                           
        self.R = args.R   
        self.D = args.D
        self.time_days = args.TD                        
        self.total_people = args.TP         
        self.sigma = args.sig                    
        self.gamma =  args.gam                   
        self.mu = args.mu                           
        self.prob_Meeting_New_Person = args.prob    
        self.number_People_Encountered = args.numb   
        self.runAll()
    

    def getPrimaryDeriv(self, initial_conditions, time, params):
        '''Arrange initial parameters into calculation  differential equations 

        args:
            initial_conditinons: Tuple of initial number of exposed, infected, recovered, and dead people in simulation
            time: Time of simultation in days
            params: Tuple of initial beta, sigma, gamma, and mu values
        returns:
            list of S, E, I, R, D values at each time point of simulation (this is a list of lists)
        '''
        self.E, self.I, self.R, self.D, self.N = self.initial_conditions
        self.S = self.N - (self.E + self.I + self.R + self.D)
        self.beta, self.sigma, self.gamma, self.mu = self.params
        self.primary_results = odeint(func = self.takeDeriv, y0 = [self.S, self.E, self.I, self.R, self.D], \
            t = self.time, args=(self.beta, self.gamma, self.sigma, self.mu))
        self.primary_resultsLIST = self.primary_results.tolist()
        return self.primary_resultsLIST 
  
    def takeDeriv(self, initial_value, t, beta, sigma, gamma, mu):
        '''Perform ordinary differential equations 

        args:
            initial_value: tuple of S, E, I, R, D values 
            for all other arguments see 'init' method

        returns:
            Results of ordinary differential equations for S, E, I, R, D values at every time point of the simulation
        '''
        self.S, self.E, self.I, self.R, self.D = initial_value
        self.N = self.S + self.E + self. I + self.R + self.D
        self.dSdt = (-self.beta * self.S * self.I )/ self.N
        self.dEdt = ((self.beta * self.S * self.I )/ self.N) - self.sigma * self.E
        self.dIdt = self.sigma * self.E - self.gamma * self.I - self.mu * self.I
        self.dRdt = self.gamma * self.I
        self.dDdt = self.mu * self.I
        return self.dSdt, self.dEdt, self.dIdt, self.dRdt, self.dDdt
    
 
    def makeCoordsandPlot(self, results, t, total_people, time_days):
        '''This method is only used for trial and erroring graph formation by callinf DSEIR.py. This method is not called from main.py
            This method can be used to plot a graph of the results by calling DSEIR.py from the command line. Will require a reworking of logic to use. Again, only used for testing purposes.

        args:
            t: grid of time points for simulation
            time_days: Length of simulation in days
            total_people: Total population size
        returns:
            graph of results made using matPlotLib
        '''
        i=0
        for value in results:
            value.append(t[i])
            i += 1 
        fig, ax = plt.subplots()
        ax.set_xlim(0,time_days)
        ax.set_ylim(0,total_people)
        lineS, = ax.plot(0,0)
        lineE, = ax.plot(0,0)
        lineI, = ax.plot(0,0)
        lineR, = ax.plot(0,0)
        lineD, = ax.plot(0,0)
        lineS.set_label('Susceptible')
        lineE.set_label('Exposed')
        lineI.set_label('Infected')
        lineR.set_label('Recovered')
        lineD.set_label('Dead')
        ax.legend(loc = 'center right')

     
        def animation_frame(self, results, e):
            '''Makes graph using lines defined above. 

            args:
                results: list of lists of S, E, I, R, D values at each time point to be plotted
                e: timekeeper value from 'timekeeper' class
            returns:
                End graph of simulation
            '''
            lineS.set_data(Tx[0:e.timestep], Sy[0:e.timestep])
            lineE.set_data(Tx[0:e.timestep], Ey[0:e.timestep])
            lineI.set_data(Tx[0:e.timestep], Iy[0:e.timestep])
            lineR.set_data(Tx[0:e.timestep], Ry[0:e.timestep])
            lineD.set_data(Tx[0:e.timestep], Dy[0:e.timestep])
            e.timestep += 1

            return lineS, lineE, lineI, lineR, lineD,
        
        timestep = timekeeper()
        animation = FuncAnimation(fig, func = animation_frame,  fargs = [results, timestep], interval = 100)
        plt.show()
        
    def getDSEIR(self):
        '''Makes a list of individual S, E, I, R, and D values to be used in simulation.py. 

        returns:
            Individual list of S, E, I, R, D values at each time point to be used in the simulation
        '''
        Sy, Ey, Iy, Ry, Dy = [], [], [], [], [],
        for value in self.primary_results:
            Sy.append(value[0])
            Ey.append(value[1])
            Iy.append(value[2])
            Ry.append(value[3])
            Dy.append(value[4])
        return Sy, Ey, Iy, Ry, Dy


    def runAll(self):
        '''Get the whole party started by calling functions and formatting data to be used in simulation. 

        beta: rate at which infectionus people interact with each other = reproduction number * gamma 

        '''
        self.time = np.linspace(0, self.time_days, self.time_days +1) 
        self.beta =  self.prob_Meeting_New_Person * self.number_People_Encountered   
        self.params = self.beta, self.sigma, self.gamma, self.mu                           
        self.initial_conditions = self.E, self.I, self.R, self.D, self.total_people      
        self.primaryResults = self.getPrimaryDeriv(self.initial_conditions, self.time, self.params)

class timekeeper():
    def __init__(self):
        self.timestep = 0

if __name__ == "__main__":
    seird = DSEIR(args)
    seird.runAll()
