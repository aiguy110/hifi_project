import matplotlib.pyplot as plt
import numpy as np
import os
from scipy.optimize import minimize

in_file = 'ethanol_sensor.csv'
bacs = []
voltages = []
highest_voltage = -1
with open(in_file, 'r') as f:
    for i, line in enumerate(f):
        if i == 0: # Skip the the first row. It holds the labels
            continue
        bac, raw_level = list(map(float, line.split(',')))
        voltage = 5*raw_level/1024
        bacs.append(bac)
        voltages.append(voltage)
        if voltage > highest_voltage:
            highest_voltage = voltage


def line_error(params):
    m, b = params
    total_error = 0
    for i in range(len(bacs)):
        total_error += abs(m*raw_levels[i]+b - bacs[i])
    return total_error

best_m, best_b = minimize(line_error, [0.0, 0.0]).x

# Plot points
plt.plot(voltages, bacs, 'o')

# Plot line
x = np.array([0, highest_level*1.2])
print( x,best_m, best_b)
print(x*best_m)
y = best_m*x + best_b
plt.plot(x,y, '-')

plt.show()
