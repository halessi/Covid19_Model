# SEIRD Model of COVID 19 Transmission


This libary was created to vidually model the spread of COVID19 in a population using the SEIRD compartmental model. By using real world values realated to COVID19, such as death rate, time of asymptomatic infection, and average duration of infection the dynamics of diseae transmission can be modeled. For any questions or comments, please reach out to ***h_alessi@coloradocollege.edu*** or ***g_nahass@coloradocollege.edu***.

This model was created more as a visual tool to demonstrate the utility of social distancing in regard to preventing massive hospital overflow and the overall rate of disease progession throughout a population. As such, this model should not be used to inform any personal health decisions as it does not take into consideration countless other varibles that affect COVID19 spread. Please consult the CDC for the most up to date information regarding COVID19.

### Dependencies

 ```pip install numpy scipy matplotlib argparse utils person math'''

### Basic usage

As of now, command line arguments are used to parse parameters. See main.py for default values. Here is a description of the parameters: (as of now)

```
python main.py \
        --exposed        
        --infected        
        --recovered         
        --dead      
        --time_days 
        --total_people         
        --sigma      
        --gamma 
        --mu 
        --prob_people 
        --numb_people
```
  Argument              | Usage          
----------------------- | ------------------
exposed                 | Initial number of exposed people
infected                | Initial number infected people
recovered               | Initial number recovered people
dead                    | Initial number dead people
time_days               | Time of simulation in days
total_people            | Total population size
sigma                   | Rate of latent individuals becoming infectious = 1/average asympotmatic incubation
gamma                   | Recovery rate == 1/duration of infection = gamma
mu                      | Death rate
prob_people             | beta knot= probability of infection if meeting an infected person
numb_people              | Average total number of people encountered

### Example

If you want to run a simulation comtaining 100000 individuals with 2 initial exposed people over a time period of 150 days, 0 initial infected, recovered, and dead peple (default values), with sigma, gamma, mu values of .15, .1, and .004 respectively , and the probablity of infection if meeting an infected person is .095, and the average number of people a subject encounters per day to be 15 we can run:

python main.py --exposed 2 --time_days 150 --total_people 100000 --sigma .15 --gamma .1 --mu .004 --prob_people .095 --numb_people 15

There will be no temrinal output, just a plot of the simulation that will pop up.
