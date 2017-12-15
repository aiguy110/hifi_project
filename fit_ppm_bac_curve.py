import matplotlib.pyplot as plt
import numpy as np
import os
from scipy.optimize import minimize

in_file = 'ethanol_sensor.csv'
bacs = []
ppms = []
highest_ppm = -1
with open(in_file, 'r') as f:
    for i, line in enumerate(f):
        if i == 0: # Skip the the first row. It holds the labels
            continue
        bac, raw_level = list(map(float, line.split(',')))
        voltage = raw_level / 1024 * 5
        ppm = np.exp(-14.7*((5/3.3 - 1)/(5/voltage - 1) - 0.45))
        bacs.append(bac)
        ppms.append(ppm)
        if ppm > highest_ppm:
            highest_ppm = ppm


def line_error(params):
    m, b = params
    total_error = 0
    for i in range(len(bacs)):
        total_error += abs(m*ppms[i]+b - bacs[i])
    return total_error

best_m, best_b = minimize(line_error, [0.0, 0.0]).x

# Plot points
plt.plot(ppms, bacs, 'o')

# Plot line
x = np.array([0, highest_ppm*1.2])
print( x,best_m, best_b )
print( x*best_m )
y = best_m*x + best_b
plt.plot(x,y, '-')
plt.ylabel('BAC (%)')
plt.xlabel('ethanol (ppm)')
plt.title(f'm={best_m:.{4}}, b={best_b:.{4}}')
plt.show()
