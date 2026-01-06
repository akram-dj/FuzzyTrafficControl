import numpy as np
import matplotlib.pyplot as plt
import skfuzzy as fuzz

# Universe of discourse
cars_universe = np.arange(0, 51, 1)

# Membership functions
low = fuzz.trimf(cars_universe, [0, 0, 15])
medium = fuzz.trimf(cars_universe, [10, 25, 40])
high = fuzz.trimf(cars_universe, [30, 50, 50])

# Plotting
plt.figure()
plt.plot(cars_universe, low, label='Low')
plt.plot(cars_universe, medium, label='Medium')
plt.plot(cars_universe, high, label='High')

plt.title("Fuzzy Membership Functions for Cars")
plt.xlabel("Number of Cars")
plt.ylabel("Membership Degree")
plt.legend()
plt.grid(True)
plt.show()
