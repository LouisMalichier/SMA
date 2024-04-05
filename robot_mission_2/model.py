#Group n°2
#22/03/2024
#Members : Badard Alexis, Malichier Louis, Saudreau Nicolas, Maamar Marouane

from mesa import Model, DataCollector
from mesa.space import MultiGrid
from mesa.time import RandomActivation
from agents import GreenRobot  # Ensure this import matches your project structure
from objects import Waste , WasteDisposalZone  
from schedule import RandomActivationScheduler
import random

class SimpleRobotMission(Model):
    def __init__(self, width=3, height=3, initial_waste=4):
        super().__init__() 
        self.grid = MultiGrid(width, height, False)
        self.schedule = RandomActivationScheduler(self)

        # Initialize a Green Robot at a random position
        robot = GreenRobot(self.schedule.get_agent_count(), self)
        self.schedule.add(robot)
        self.grid.place_agent(robot, (random.randrange(width), random.randrange(height)))

        # Randomly place initial green waste
        for _ in range(initial_waste):
            waste = Waste(self.schedule.get_agent_count(), self, waste_type="green")
            while True:
                pos = (random.randrange(width), random.randrange(height))
                if self.grid.is_cell_empty(pos):
                    self.grid.place_agent(waste, pos)
                    self.schedule.add(waste)
                    break

        # Define a disposal zone location at the far east of the grid
        self.disposal_zone = (width - 1, random.randrange(height))
        disposal_zone_agent = WasteDisposalZone(self.schedule.get_agent_count(), self)
        self.grid.place_agent(disposal_zone_agent, self.disposal_zone)
        self.datacollector = DataCollector(
            {
                "GreenRobot": lambda m: m.schedule.get_type_count(GreenRobot),
                "Waste": lambda m: m.schedule.get_type_count(Waste),
            }
        )
        self.schedule.add(disposal_zone_agent)

    def step(self):
        self.schedule.step()
        self.datacollector.collect(self)
        # self verbose if needed


    def perform_action(self, agent, action):
        """Model processes the action requested by the agent."""
        if action == "collect_waste":
            contents = self.grid.get_cell_list_contents(agent.pos)
            for content in contents:
                if isinstance(content, Waste) and len(agent.knowledge["collected_waste"]) < 2:
                    agent.knowledge["collected_waste"].append(content)
                    print(agent.knowledge["collected_waste"])
                    self.grid.remove_agent(content)
                    break
        elif action == "transform_waste":
            yellow_waste = Waste(self.schedule.get_agent_count(), self, waste_type="yellow")
            self.schedule.add(yellow_waste)
            agent.knowledge["collected_waste"][0] = yellow_waste
            agent.knowledge["collected_waste"] = agent.knowledge["collected_waste"][:1]
            print(agent.knowledge["collected_waste"])
        elif action == "dispose_waste":
    # Check if the agent is at the disposal zone
            if agent.pos == self.disposal_zone:
                # Go through the collected waste to find a yellow one to dispose of
                for waste in agent.knowledge["collected_waste"]:
                    if waste.waste_type == "yellow":
                        # Remove the disposed waste from the robot's knowledge
                        agent.knowledge["collected_waste"].remove(waste)
                        # Create a new yellow Waste agent in the disposal zone
                        self.grid.place_agent(waste, self.disposal_zone)
                        print(agent.knowledge["collected_waste"])
                        break  # Assuming we only dispose of one waste at a time
                        
            else:
                # Move towards disposal zone
                self.move_agent_towards_disposal_zone(agent)
    def move_agent_towards_disposal_zone(self, agent):
        """Move the agent one step towards the disposal zone."""
        x, y = agent.pos
        dx, dy = self.disposal_zone
        # Move horizontally towards dx
        if x < dx:
            new_x = x + 1
        elif x > dx:
            new_x = x - 1
        else:
            new_x = x
        # Move vertically towards dy
        if y < dy:
            new_y = y + 1
        elif y > dy:
            new_y = y - 1
        else:
            new_y = y
        # Update the agent's position
        agent.model.grid.move_agent(agent, (new_x, new_y))


        
