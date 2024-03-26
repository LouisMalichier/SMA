from model_Louis import environment
from visualize import *

model = environment()  # 10x10 grid with 2 green, 2 yellow, and 2 red robots
model.run_model()

#Visualization
data=model.datacollector.get_model_vars_dataframe()
print_waste_per_step(data, model.initial_robot)