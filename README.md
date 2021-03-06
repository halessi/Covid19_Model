# SEIRD Model of COVID 19 Transmission


This libary was created to visually model the spread of COVID19 in a population using the SEIRD compartmental model. By using real world values related to COVID19, such as death rate, time of asymptomatic infection, and average duration of infection, the dynamics of disease transmission can be modeled. For any questions or comments, please reach out to ***h_alessi@coloradocollege.edu*** or ***g_nahass@coloradocollege.edu***.

This model was created more as a visual tool to demonstrate the utility of social distancing in regard to preventing massive hospital overflow and the overall rate of disease progession throughout a population. As such, this model should not be used to inform any personal health decisions as it does not take into consideration countless other varibles that affect COVID19 spread. Please consult the CDC for the most up to date information regarding COVID19.

### Dependencies

 ```pip install numpy scipy matplotlib argparse utils math```

### Basic usage

As of now, command line arguments are used to parse parameters. See main.py for default values. Here is a description of the parameters: 

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
prob_people             | Beta knot= probability of infection if meeting an infected person
numb_people             | Average total number of people encountered


### Example

If you want to run a simulation comtaining 3600 individuals with 1 initial exposed people over a time period of 100 days, 0 initial infected, recovered, and dead peple (default values), with sigma, gamma, mu values of .143, .095, and .0034 respectively, the probablity of infection if meeting an infected person is .1, and the average number of people a subject encounters per day to be 10, we can run:

```python main.py --exposed 1 --time_days 100 --total_people 3600 --sigma .143 --gamma .095 --mu .0034 --prob_people .1 --numb_people 10```

Terminal output indicates when the value used to assign dot color values does not equal the value used in the simulation and line plot. The main result will be a plot of the simulation that will pop up (example from above shown below). Have fun!

![Optional Text](../master/images/numb=10.gif)

Below is a panel created by running simulations with varying valus for the average number of people contacted per day (--numb_people)  

![Optional Text](../master/images/covid_gif3.gif)

### References
[1] https://www.medrxiv.org/content/10.1101/2020.04.02.20050674v2.full.pdf \
[2] https://towardsdatascience.com/simulating-compartmental-models-in-epidemiology-using-python-jupyter-widgets-8d76bdaff5c2 \
[3] https://triplebyte.com/blog/modeling-infectious-diseases \
[4] https://arxiv.org/pdf/2002.06563.pdf \
[5] https://www.medrxiv.org/content/10.1101/2020.03.27.20045005v3.full.pdf \
