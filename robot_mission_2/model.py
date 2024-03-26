#Group n°2
#22/03/2024
#Members : Badard Alexis, Malichier Louis, Saudreau Nicolas, Maamar Marouane

from mesa import Model
from mesa.space import MultiGrid
from mesa.time import RandomActivation
from agents import GreenRobot, Waste  # Ensure this import matches your project structure
import random

class SimpleRobotMission(Model):
    def __init__(self, width=3, height=3, initial_waste=4):
        super().__init__() 
        self.grid = MultiGrid(width, height, True)
        self.schedule = RandomActivation(self)

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

    def step(self):
        self.schedule.step()

    def perform_action(self, agent, action):
        """Model processes the action requested by the agent."""
        if action == "collect_waste":
            contents = self.grid.get_cell_list_contents(agent.pos)
            for content in contents:
                if isinstance(content, Waste):
                    self.grid.remove_agent(content)  # Remove waste from grid
                    self.model.schedule.remove(content)
                    if hasattr(self, 'collector'):
                        self.collector.remove_agent(content) 
                    agent.knowledge["collected_waste"] += 1
        elif action == "dispose_waste":
            # If the agent is at the disposal zone, reset collected waste
            if agent.pos == self.disposal_zone:
                agent.knowledge["collected_waste"] = 0
            else:
                # Move towards disposal zone
                self.move_agent_towards_disposal_zone(agent)
        # Implement 'move_randomly' in the agent's 'move' method
        elif action == 'move_randomly':
            self.move_randomly(agent)

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
    
    def move_randomly(self,agent):
        """Move the agent to a random neighboring cell."""
        x, y = agent.pos
        possible_steps = self.grid.get_neighborhood((x, y), moore=False, include_center=False)
        new_position = self.random.choice(possible_steps)
        self.grid.move_agent(agent, new_position)