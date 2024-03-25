from mesa import Agent, Model
from mesa.space import MultiGrid
from mesa.time import RandomActivation
import random

from model_Nicolas import WasteModel

model = WasteModel(10, 10, 2, 2, 2)  # 10x10 grid with 2 green, 2 yellow, and 2 red robots
for i in range(10):
    model.step()