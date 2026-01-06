import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt
# Define fuzzy variables
cars = ctrl.Antecedent(np.arange(0, 51, 1), 'cars')
green_time = ctrl.Consequent(np.arange(5, 31, 1), 'green_time')

# Define membership functions for cars
cars['low'] = fuzz.trimf(cars.universe, [0, 0, 15])
cars['medium'] = fuzz.trimf(cars.universe, [10, 25, 40])
cars['high'] = fuzz.trimf(cars.universe, [30, 50, 50])

# Define membership functions for green_time
green_time['short'] = fuzz.trimf(green_time.universe, [5, 5, 12])
green_time['medium'] = fuzz.trimf(green_time.universe, [10, 17, 24])
green_time['long'] = fuzz.trimf(green_time.universe, [20, 30, 30])

# Define fuzzy rules
rules = [
    ctrl.Rule(cars['low'], green_time['short']),
    ctrl.Rule(cars['medium'], green_time['medium']),
    ctrl.Rule(cars['high'], green_time['long']),
]

# Create control system
system = ctrl.ControlSystem(rules)
sim = ctrl.ControlSystemSimulation(system)

def fuzzy_decision(car_count):
    """
    Calculate optimal green time based on vehicle count
    
    Args:
        car_count: Number of vehicles waiting in a direction
        
    Returns:
        Optimal green light time in seconds
    """
    sim.input['cars'] = min(car_count, 50)
    sim.compute()
    return round(sim.output['green_time'])
def get_next_green_signal(vehicle_counts):
    """
    Determine which signal should turn green next based on vehicle counts
    
    Args:
        vehicle_counts: Dictionary with direction numbers as keys and vehicle counts as values
        
    Returns:
        Tuple of (direction_number, green_time)
    """
    # Find direction with maximum vehicles
    max_direction = max(vehicle_counts, key=vehicle_counts.get)
    max_count = vehicle_counts[max_direction]
    
    # Calculate green time for that direction
    green_time = fuzzy_decision(max_count)
    
    return max_direction, green_time
