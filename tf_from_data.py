import matplotlib.pyplot as plt
import numpy as np
import os
from scipy.optimize import minimize

class RunData:
    def __init__(self, filename):
        # Parameters to fit to data
        self.start_time = 10.0
        self.start_val = 0.0
        self.end_val = 1.0
        self.tau = 1.0

        # Load data from file
        self.temperature_data = []
        with open(filename, 'r') as f:
            for line in f:
                temperature = float(line.split(',')[1])
                self.temperature_data.append(temperature)
        self.temperature_data = self.temperature_data[::-1] # Waveforms saved the data backwards.

    def fit_func(self, n, param_vector=None):
        if param_vector is None:
            param_vector = self.get_param_vector()
        start_time, start_val, end_val, tau = param_vector

        if n < start_time:
            return start_val
        else:
            return end_val + (start_val - end_val)*np.exp(-(n-start_time)/tau)

    def get_param_vector(self):
        return [self.start_time, self.start_val, self.end_val, self.tau]

    def set_param_vector(self, param_vector):
        self.start_time, self.start_val, self.end_val, self.tau = param_vector

    def get_error(self, param_vector=None):
        if param_vector is None:
            param_vector = self.get_param_vector(param_vector)

        total_error = 0
        for i in range(len(self.temperature_data)):
            total_error += abs(self.fit_func(i, param_vector) - self.temperature_data[i])
        return total_error

    def fit(self):
        best_params = minimize(self.get_error, self.get_param_vector()).x
        self.set_param_vector(best_params)

    def plot(self):
        # Plot the data
        n = np.arange(len(self.temperature_data))
        plt.plot(n, self.temperature_data, 'o')

        # Plot the best fitting curve
        fit_points = np.zeros(len(self.temperature_data))
        for i in range(len(fit_points)):
            fit_points[i] = self.fit_func(i)
        plt.plot(n, fit_points)



data_files = ['data/'+fname for fname in os.listdir('data') if fname[-4:] == '.csv']
runs = []
for n, fname in enumerate(data_files):
    print(f'Loading run {fname} as {n}')
    runs.append(RunData(fname))


run_count = len(runs)
average_tau = 0
for n, run in enumerate(runs):
    print(f'Processing run {n}')
    run.fit()
    plt.subplot(run_count, 1, n+1)
    run.plot()
    plt.ylabel('Voltage (V)')
    plt.xlabel('Time (s)')

    average_tau += run.tau
average_tau /= run_count

fig.suptitle(f'Best Fits (average_tau={average_tau:.{4}f})')
plt.show()
