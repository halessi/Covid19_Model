import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

class SEIRD():
    ###  SIMULATION SETUP ###
    def __init__(self):
        self.E = 1                           #initial number of exposed people
        self.I = 0                           #initial number infected people 
        self.R = 0   
        self.D = 0
        self.time_days = 100                        #Initial number recovered people
        self.total_people = 100000         #total population soize
        self.sigma = .143                    #Rate of latent individuals becoming infected
        self.gamma =  .095                   #recovery/ mortality rate == 1/duration of infection = gamma
        self.mu = .0034              #Death rate
        self.prob_Meeting_New_Person = .1     #beta knot= probability of infection if meeting an infected person
        self.number_People_Encountered = 25    #k = total number of people encountered
    
   
    def getPrimaryDeriv(self, initial_conditions, time, params):
        self.E, self.I, self.R, self.D, self.N = self.initial_conditions
        self.S = self.N - (self.E + self.I + self.R + self.D)
        self.beta, self.sigma, self.gamma, self.mu = self.params

        self.primary_results = odeint(func = self.takeDeriv, y0 = [self.S, self.E, self.I, self.R, self.D], \
            t = self.time, args=(self.beta, self.gamma, self.sigma, self.mu))
        self.primary_resultsLIST = self.primary_results.tolist()
        return self.primary_resultsLIST 

    def takeDeriv(self, initial_value, t, beta, sigma, gamma, mu):
        print(initial_value)
        self.S, self.E, self.I, self.R, self.D = initial_value
        self.N = self.S + self.E + self. I + self.R + self.D
        self.dSdt = (-self.beta * self.S * self.I )/ self.N
        self.dEdt = ((self.beta * self.S * self.I )/ self.N) - self.sigma * self.E
        self.dIdt = self.sigma * self.E - self.gamma * self.I - self.mu * self.I
        self.dRdt = self.gamma * self.I
        self.dDdt = self.mu * self.I
        return self.dSdt, self.dEdt, self.dIdt, self.dRdt, self.dDdt


    def makeCoordsandPlot(self, results, t, total_people, time_days):
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

        Sy, Ey, Iy, Ry, Dy, Tx   = [], [], [], [], [], []
        
        for value in results:
            Sy.append(value[0])
            Ey.append(value[1])
            Iy.append(value[2])
            Ry.append(value[3])
            Dy.append(value[4])
            Tx.append(value[5])

        def animation_frame(self, results, e):
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
        
    def runAll(self):
        self.time = np.linspace(0, self.time_days, self.time_days +1) #grid of time points for simulation
        self.beta =  self.prob_Meeting_New_Person * self.number_People_Encountered   #rate at which infectionus people interact with each other = reproduction number * gamma 
        self.params = self.beta, self.sigma, self.gamma, self.mu                             #parameter tuple to be unpacked to calculate dif eqs
        self.initial_conditions = self.E, self.I, self.R, self.D, self.total_people      #initial conditions of simulation tuple to be unpacked for dif eqs
        self.primaryResults = self.getPrimaryDeriv(self.initial_conditions, self.time, self.params)
        self.makeCoordsandPlot(self.primaryResults, self.time, self.total_people, self.time_days)

class timekeeper():
    def __init__(self):
        self.timestep = 0

if __name__ == "__main__":
    seird = SEIRD()
    seird.runAll()
