#Group n°2
#22/03/2024
#Members : Badard Alexis, Malichier Louis, Saudreau Nicolas, Maamar Marouane

from mesa import Agent
from objects_N import Waste

class GreenRobot(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.knowledge = {"collected_waste": [], "waste_here": False, "current_position": None, "seen_position":[], "unseen_position":[]}

    def percepts(self):
        """Gather information from the environment."""
        contents = self.model.grid.get_cell_list_contents([self.pos])
        waste_here = any(isinstance(c, Waste) and c.waste_type == "green" for c in contents)
        self.knowledge.update({"waste_here": waste_here, "current_position": self.pos})

    def deliberate(self, knowledge):
        """Decide on an action based on the current knowledge."""
        # If the robot is on waste and hasn't collected 2 wastes yet, collect more waste.
        if knowledge["waste_here"] and len(knowledge["collected_waste"]) < 2:
            return "collect_waste"
        # If the robot has collected 2 green wastes, it should transform them into yellow waste.
        elif len(knowledge["collected_waste"]) == 2:
            return "transform_waste"
        # If the robot has transformed the waste (implying it has 1 yellow waste), it should dispose of the waste.
        elif len(knowledge["collected_waste"]) == 1 and knowledge["collected_waste"][0].waste_type == "yellow":
            return "dispose_waste"
        # Otherwise, move randomly.
        else:
            return "move_randomly"

    def do_init(self, action):
        """Perform an action and update the environment and knowledge accordingly."""
        if action == "collect_waste" or action == "dispose_waste" or action == "transform_waste":
            self.model.perform_action(self, action)
        elif action == "move_randomly":
            possible_steps = self.model.grid.get_neighborhood(self.pos, moore=False, include_center=False)
            print("possible Green", type(possible_steps))
            new_position = self.random.choice(possible_steps)
            self.model.move_robot(self, new_position)

    def do_V1(self, action):
        """Perform an action and update the environment and knowledge accordingly."""
        if action == "collect_waste" or action == "dispose_waste" or action == "transform_waste":
            self.model.perform_action(self, action)
        elif action == "move_randomly":
            possible_steps = self.model.grid.get_neighborhood(self.pos, moore=False, include_center=False)
            print("possible Green", possible_steps)
            new_position = possible_steps[0]
            n = 1
            while not self.model.is_position_allowed(self, new_position):
                new_position = possible_steps[n]
                n = n+1

            if not self.model.is_position_allowed(self, new_position) : new_position = self.random.choice(possible_steps) 
            #new_position = self.model.choose_next_position(self)
            print("new_position choose", new_position)
            self.model.move_robot(self, new_position)


    def do(self, action):
            """Perform an action and update the environment and knowledge accordingly."""
            if action == "collect_waste" or action == "dispose_waste" or action == "transform_waste":
                self.model.perform_action(self, action)
            elif action == "move_randomly":
        
                #possible_steps = self.model.grid.get_neighborhood(self.pos, moore=False, include_center=False)
                new_position = self.model.choose_next_position_Snake(self)
                print("Green new position", new_position)
                self.model.move_robot(self, new_position)

    def step(self):
        percepts = self.percepts()
        action = self.deliberate(self.knowledge)
        self.do(action)

class YellowRobot(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.knowledge = {"collected_waste": [], "waste_here": False, "current_position": None}

    def percepts(self):
        """Gather information from the environment."""
        contents = self.model.grid.get_cell_list_contents([self.pos])
        waste_here = any(isinstance(c, Waste) and c.waste_type == "yellow" for c in contents)
        self.knowledge.update({"waste_here": waste_here, "current_position": self.pos})

    def deliberate(self, knowledge):
        """Decide on an action based on the current knowledge."""
        # If the robot is on waste and hasn't collected 2 wastes yet, collect more waste.
        if knowledge["waste_here"] and len(knowledge["collected_waste"]) < 2:
            return "collect_waste"
        # If the robot has collected 2 green wastes, it should transform them into yellow waste.
        elif len(knowledge["collected_waste"]) == 2:
            return "transform_waste"
        # If the robot has transformed the waste (implying it has 1 yellow waste), it should dispose of the waste.
        elif len(knowledge["collected_waste"]) == 1 and knowledge["collected_waste"][0].waste_type == "red":
            return "dispose_waste"
        # Otherwise, move randomly.
        else:
            return "move_randomly"

    def do_initial(self, action):
        """Perform an action and update the environment and knowledge accordingly."""
        if action == "collect_waste" or action == "dispose_waste" or action == "transform_waste":
            self.model.perform_action(self, action)
        elif action == "move_randomly":
            possible_steps = self.model.grid.get_neighborhood(self.pos, moore=False, include_center=False)
            new_position = self.random.choice(possible_steps)
            self.model.move_robot(self, new_position)

    def do(self, action):
        """Perform an action and update the environment and knowledge accordingly."""
        if action == "collect_waste" or action == "dispose_waste" or action == "transform_waste":
            self.model.perform_action(self, action)
        elif action == "move_randomly":
            target = (6,6)
            #possible_steps = self.model.grid.get_neighborhood(self.pos, moore=False, include_center=False)
            #new_position = self.model.choose_next_position(self, target[0], target[1])
            new_position = self.model.choose_next_position_Snake(self)
            print("Yellow new position", new_position)
            self.model.move_robot(self, new_position)



    def step(self):
        percepts = self.percepts()
        action = self.deliberate(self.knowledge)
        self.do(action)

class RedRobot(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.knowledge = {"collected_waste": [], "waste_here": False, "current_position": None}

    def percepts(self):
        """Gather information from the environment."""
        contents = self.model.grid.get_cell_list_contents([self.pos])
        waste_here = any(isinstance(c, Waste) and c.waste_type == "red" for c in contents)
        self.knowledge.update({"waste_here": waste_here, "current_position": self.pos})

    def deliberate(self, knowledge):
        """Decide on an action based on the current knowledge."""
        if knowledge["waste_here"] and len(knowledge["collected_waste"]) == 0:
            return "collect_waste" 
        elif len(knowledge["collected_waste"]) == 1:
            return "dispose_waste"
        # Otherwise, move randomly.
        else:
            return "move_randomly"

    def do(self, action):
        """Perform an action and update the environment and knowledge accordingly."""
        if action == "collect_waste" or action == "dispose_waste" :
            self.model.perform_action(self, action)
        elif action == "move_randomly":
            possible_steps = self.model.grid.get_neighborhood(self.pos, moore=False, include_center=False)
            new_position = self.random.choice(possible_steps)
            self.model.move_robot(self, new_position)

    def step(self):
        percepts = self.percepts()
        action = self.deliberate(self.knowledge)
        self.do(action)



