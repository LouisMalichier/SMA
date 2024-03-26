#Group n°2
#22/03/2024
#Members : Badard Alexis, Malichier Louis, Saudreau Nicolas, Maamar Marouane

from mesa import Agent
from objects import Waste

class GreenRobot(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.knowledge = {"collected_waste": 0, "waste_here": False, "current_position": None}

    def percepts(self):
        """Gather information from the environment."""
        contents = self.model.grid.get_cell_list_contents([self.pos])
        waste_here = any(isinstance(c, Waste) for c in contents)
        self.knowledge.update({"waste_here": waste_here, "current_position": self.pos})

    def deliberate(self, knowledge):
        """Decide on an action based on the current knowledge."""
        if knowledge["waste_here"] and knowledge["collected_waste"] < 2:
            return "collect_waste"
        elif knowledge["collected_waste"] >= 2:
            return "dispose_waste"
        else:
            return "move_randomly"

    def do(self, action):
        """Perform an action and update the environment and knowledge accordingly."""
        if action == "collect_waste":
            self.knowledge["collected_waste"] += 1
            # Code to remove a waste instance from the grid goes here
        elif action == "dispose_waste":
            # Code to move towards disposal zone and dispose waste goes here
            pass
        elif action == "move_randomly":
            self.move()

    def move(self):
        possible_steps = self.model.grid.get_neighborhood(self.pos, moore=False, include_center=False)
        new_position = self.random.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)

    def step(self):
        percepts = self.percepts()
        action = self.deliberate(self.knowledge)
        self.do(action)