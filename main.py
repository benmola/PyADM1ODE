# -*- coding: utf-8 -*-
"""
Created on Fri Nov 04 09:56:06 2023

@author: Daniel Gaida
"""

from PyADM1 import get_state_zero_from_initial_state, PyADM1

from feedstock import Feedstock

from Simulator import Simulator

feeding_freq = 48   # every feeding_freq hours the controller can change the substrate feed of the digester

myfeedstock = Feedstock(feeding_freq)

adm1 = PyADM1(myfeedstock)
mySimulator = Simulator(adm1)

# initial substrate feed for all substrates. At the moment only values for the first two substrates may be changed, rest 0
# first value: corn silage, 2nd value: liquid manure, both in m^3/d
Q = [15, 10, 0, 0, 0, 0, 0, 0, 0, 0]
#Q = [69, 64, 0, 0, 0, 0, 0, 0, 0, 0]

# initial ADM1 state vector where to start the simulation
state_zero = get_state_zero_from_initial_state("digester_initial8.csv")

## time array definition
t = myfeedstock.simtime()

# Initiate the cache data frame for storing simulation results
simulate_results = [state_zero]

t0=0

## Dynamic simulation
# Loop for simulating at each time step and feeding the results to the next time step
for n, u in enumerate(t[1:], 1):
    # you could change Q here to simulate with dynamically changing substrate feed

    adm1.createInfluent(Q, n)

    # Span for next time step
    tstep = [t0,u]

    state_zero = mySimulator.simulateADplant(tstep, state_zero)

    simulate_results.append(state_zero)

    t0 = u

    if n % 100 == 0:
        print("Simulated {0} of {1} steps.".format(n, len(t)))

# save final ADM1 state vector
adm1.save_final_state_in_csv(simulate_results)

import matplotlib.pyplot as plt
import pandas as pd

def plot_results(adm1, t, simulate_results):
    # Calculate plotting data from simulation results
    data = [adm1.get_state_variables(s) for s in simulate_results]
    
    # Save to CSV
    df = pd.DataFrame(data)
    df['time'] = t
    # Reorder columns to put time first
    cols = ['time'] + [col for col in df.columns if col != 'time']
    df = df[cols]
    df.to_csv('simulation_outputs.csv', index=False)
    print("Simulation outputs saved to simulation_outputs.csv")

    # Extract lists for plotting
    Q_GAS = [d['Q_gas'] for d in data]
    Q_CH4 = [d['Q_ch4'] for d in data]
    P_GAS = [d['P_gas'] for d in data]
    pH = [d['pH'] for d in data]
    FOS_TAC = [d['FOS_TAC'] for d in data]
    Ac_Pro = [d['Ac_Pro'] for d in data]
    VFA = [d['VFA'] for d in data]
    TAC = [d['TAC'] for d in data]
    SS = [d['SS'] for d in data]
    VS = [d['VS'] for d in data]
    Biomass = [d['Biomass'] for d in data]

    # Figure 1: Gas Production
    plt.figure(1, figsize=(10, 6))
    plt.subplot(2, 1, 1)
    plt.plot(t, Q_GAS, label='Gas')
    plt.plot(t, Q_CH4, label='CH4')
    plt.legend()
    plt.ylabel('Flow [m3/d]')
    plt.title('Gas Production')
    plt.grid(True)

    plt.subplot(2, 1, 2)
    plt.plot(t, P_GAS, label='Pressure')
    plt.legend()
    plt.ylabel('Pressure [bar]')
    plt.xlabel('time [d]')
    plt.grid(True)

    # Figure 2: Stability Indicators
    plt.figure(2, figsize=(10, 8))
    plt.subplot(3, 1, 1)
    plt.plot(t, pH, label='pH')
    plt.legend()
    plt.ylabel('pH [-]')
    plt.title('Stability Indicators')
    plt.grid(True)

    plt.subplot(3, 1, 2)
    plt.plot(t, FOS_TAC, label='FOS/TAC')
    plt.plot(t, Ac_Pro, label='Ac/Pro')
    plt.legend()
    plt.ylabel('Ratio [-]')
    plt.grid(True)

    plt.subplot(3, 1, 3)
    plt.plot(t, VFA, label='VFA [gHAceq/l]')
    plt.plot(t, TAC, label='TAC [gCaCO3eq/l]')
    plt.legend()
    plt.ylabel('Concentration')
    plt.xlabel('time [d]')
    plt.grid(True)

    # Figure 3: Solids and Biomass
    plt.figure(3, figsize=(10, 6))
    plt.subplot(2, 1, 1)
    plt.plot(t, SS, label='SS')
    plt.plot(t, VS, label='VS')
    plt.legend()
    plt.ylabel('Concentration [kg/m3]')
    plt.title('Solids and Biomass')
    plt.grid(True)

    plt.subplot(2, 1, 2)
    plt.plot(t, Biomass, label='Biomass')
    plt.legend()
    plt.ylabel('Concentration [kg/m3]')
    plt.xlabel('time [d]')
    plt.grid(True)

    plt.show()

plot_results(adm1, t, simulate_results)
