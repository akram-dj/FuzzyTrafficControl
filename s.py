# FULL FUZZY INFERENCE + DEFUZZIFICATION CODE
# Cars -> Green Time (Traffic Light)

import numpy as np
import matplotlib.pyplot as plt

# ---------- Triangular Membership Function ----------
def trimf(x, abc):
    a, b, c = abc
    y = np.zeros_like(x, dtype=float)

    if a != b:
        idx = np.logical_and(a < x, x < b)
        y[idx] = (x[idx] - a) / (b - a)

    if b != c:
        idx = np.logical_and(b < x, x < c)
        y[idx] = (c - x[idx]) / (c - b)

    y[x == b] = 1.0
    return y

# ---------- Universes ----------
cars_universe = np.arange(0, 51, 1)        # number of cars
green_universe = np.arange(5, 31, 1)       # green time (seconds)

# ---------- Membership Functions (Cars) ----------
cars_low = trimf(cars_universe, [0, 0, 15])
cars_medium = trimf(cars_universe, [10, 25, 40])
cars_high = trimf(cars_universe, [30, 50, 50])

# ---------- Membership Functions (Green Time) ----------
green_short = trimf(green_universe, [5, 5, 12])
green_medium = trimf(green_universe, [10, 17, 24])
green_long = trimf(green_universe, [20, 30, 30])

# ---------- INPUT ----------
cars_input = 20   # example: 20 cars

# ---------- FUZZIFICATION ----------
low_deg = np.interp(cars_input, cars_universe, cars_low)
med_deg = np.interp(cars_input, cars_universe, cars_medium)
high_deg = np.interp(cars_input, cars_universe, cars_high)

# ---------- RULES (Inference) ----------
# Rule 1: IF cars IS low THEN green IS short
rule1 = np.fmin(low_deg, green_short)

# Rule 2: IF cars IS medium THEN green IS medium
rule2 = np.fmin(med_deg, green_medium)

# Rule 3: IF cars IS high THEN green IS long
rule3 = np.fmin(high_deg, green_long)

# ---------- AGGREGATION ----------
aggregated = np.fmax(rule1, np.fmax(rule2, rule3))

# ---------- DEFUZZIFICATION (Centroid) ----------
defuzzified = np.sum(aggregated * green_universe) / np.sum(aggregated)

print("Cars input:", cars_input)
print("Green time (defuzzified):", round(defuzzified, 2), "seconds")

# ---------- PLOT ----------
plt.figure()
plt.plot(green_universe, green_short, '--', label='Short')
plt.plot(green_universe, green_medium, '--', label='Medium')
plt.plot(green_universe, green_long, '--', label='Long')
plt.plot(green_universe, aggregated, label='Aggregated Output', linewidth=2)
plt.axvline(defuzzified, linestyle=':', label='Defuzzified Output')

plt.title("Fuzzy Inference + Defuzzification (Green Time)")
plt.xlabel("Green Time (seconds)")
plt.ylabel("Membership Degree")
plt.legend()
plt.grid(True)
plt.show()
