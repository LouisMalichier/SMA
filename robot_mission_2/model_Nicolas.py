from mesa import Agent, Model
from mesa.space import MultiGrid
from mesa.time import RandomActivation
import random

from agent_Nicolas import Robot, Waste

class WasteModel(Model):
    def __init__(self, width, height, num_green_robots, num_yellow_robots, num_red_robots):
        self.num_green_robots = num_green_robots
        self.num_yellow_robots = num_yellow_robots
        self.num_red_robots = num_red_robots
        self.grid = MultiGrid(width, height, True)
        self.schedule = RandomActivation(self)

        # Create green robots
        for i in range(self.num_green_robots):
            x = random.randrange(width)
            y = random.randrange(height)
            robot = Robot(self.next_id(), self, "Green")
            self.grid.place_agent(robot, (x, y))
            self.schedule.add(robot)

        # Create yellow robots
        for i in range(self.num_yellow_robots):
            x = random.randrange(width)
            y = random.randrange(height)
            robot = Robot(Model.next_id(), self, "Yellow")
            self.grid.place_agent(robot, (x, y))
            self.schedule.add(robot)

        # Create red robots
        for i in range(self.num_red_robots):
            x = random.randrange(width)
            y = random.randrange(height)
            robot = Robot(Model.next_id(), self, "Red")
            self.grid.place_agent(robot, (x, y))
            self.schedule.add(robot)

        # Create wastes
        for x in range(width):
            for y in range(height):
                if x < width/3:
                    self.grid.place_agent(Waste(Model.next_id(), self, "Green"), (x, y))
                elif width/3 <= x < 2*width/3:
                    self.grid.place_agent(Waste(Model.next_id(), self, "Yellow"), (x, y))
                else:
                    self.grid.place_agent(Waste(Model.next_id(), self, "Red"), (x, y))

    def step(self):
        self.schedule.step()
