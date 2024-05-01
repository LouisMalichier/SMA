#Group n°2
#22/03/2024
#Members : Badard Alexis, Malichier Louis, Saudreau Nicolas, Maamar Marouane

from mesa import Agent
from objects import Waste
import random
from communication.agent.CommunicatingAgent import CommunicatingAgent
from communication.message.MessagePerformative import MessagePerformative
from communication.message.Message import Message
from communication.message.MessageService import MessageService

def is_in_disposal_zone(self):
        # Determine the disposal zone x-coordinate (dx) based on the robot type
        z_width = self.model.grid.width // 3
        if isinstance(self, GreenRobot):
            dx = z_width - 1   # Disposal zone for GreenRobot is at the end of z1
        elif isinstance(self, YellowRobot):
            dx = 2 * z_width - 1
        elif isinstance(self, RedRobot):
            dx = self.grid.width - 1
        # Check if the agent is at the disposal zone
        return self.pos[0] == dx

class GreenRobot(CommunicatingAgent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model, name="GreenRobot")
        self.message_service = MessageService.get_instance()
        self.knowledge = {"collected_waste": [], "waste_here": False, "current_position": None}

    def percepts(self):
        """Gather information from the environment."""
        contents = self.model.grid.get_cell_list_contents([self.pos])
        waste_here = any(isinstance(c, Waste) and c.waste_type == "green" for c in contents)
        self.knowledge.update({"waste_here": waste_here, "current_position": self.pos})

    def deliberate(self, knowledge):
        """Decide on an action based on the current knowledge."""
        # If the robot is on waste and hasn't collected 2 wastes yet, collect more waste.
        if knowledge["waste_here"] and len(knowledge["collected_waste"]) < 2 :
            if knowledge["collected_waste"] == []:
                return "collect_waste"
            elif knowledge["collected_waste"][0].waste_type == "yellow":
                return "dispose_waste"
            else:       
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
        
    def move_to_least_visited(self):
        neighbors = self.model.grid.get_neighborhood(self.pos, moore=False, include_center=False)
        allowed_neighbors = [pos for pos in neighbors if self.model.is_position_allowed(self, pos)]
        # Choose the neighbor with the least pheromones
        next_move = min(allowed_neighbors, key=lambda pos: (self.model.pheromone_levels['green'][pos], random.random()))
        return next_move

    def deposit_pheromone(self):
        x, y = self.pos
        self.model.pheromone_levels['green'][(x, y)] += 1  # Only update green pheromone levels

    def do(self, action):
        """Perform an action and update the environment and knowledge accordingly."""
        if action == "collect_waste" or action == "transform_waste":
            self.model.perform_action(self, action)
        elif action == "dispose_waste":
            # Assuming disposal location is known and is self.pos
            self.model.perform_action(self, action)
            waste_location = self.pos
            message_content = {"waste_type": "yellow", "location": waste_location}
            message = Message(from_agent=self.get_name(), to_agent="YellowRobot", message_performative=MessagePerformative.INFORM_REF, content=message_content)
            # Store message for conditional processing
            self.message_service.store_message(message)
        elif action == "move_randomly":
            #possible_steps = self.model.grid.get_neighborhood(self.pos, moore=False, include_center=False)
            new_position = self.move_to_least_visited()
            self.model.move_robot(self, new_position)
            self.deposit_pheromone()

    def step(self):
        percepts = self.percepts()
        action = self.deliberate(self.knowledge)
        self.do(action)

class YellowRobot(CommunicatingAgent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model, name=f"YellowRobot")
        self.message_service = MessageService.get_instance()
        self.knowledge = {"collected_waste": [], "waste_here": False, "current_position": None, "yellow_waste_location": None, "task_completed": False}

    def percepts(self):
        """Gather information from the environment."""
        contents = self.model.grid.get_cell_list_contents([self.pos])
        waste_here = any(isinstance(c, Waste) and c.waste_type == "yellow" for c in contents)
        self.knowledge.update({"waste_here": waste_here, "current_position": self.pos})

    def deliberate(self, knowledge):
        """Decide on an action based on the current knowledge."""
        # If the robot is on waste and hasn't collected 2 wastes yet, collect more waste.
        if self.knowledge.get("yellow_waste_location"):
            target_location = self.knowledge["yellow_waste_location"]
            if self.pos == target_location and knowledge["waste_here"]:
                if len(knowledge["collected_waste"]) < 2:
                    return "collect_waste"
                return "dispose_waste"
            else:
                return "move_to_location", target_location
        elif knowledge["waste_here"] and len(knowledge["collected_waste"]) < 2 :
            if knowledge["collected_waste"] == []:
                return "collect_waste"
            elif knowledge["collected_waste"][0].waste_type == "red":
                return "dispose_waste"
            else:
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
        
    def move_to_location(self, target_location):
        """
        Move the robot one step towards the specified target location using the model's move_robot method.
        Moves are made vertically or horizontally, prioritizing the axis with the greatest distance.
        """
        current_x, current_y = self.pos
        target_x, target_y = target_location

        # Calculate the preferred and secondary moves based on the distance
        move_x = target_x - current_x
        move_y = target_y - current_y
        
        if abs(move_x) > abs(move_y):  # Prioritize horizontal movement
            step_x = 1 if move_x > 0 else -1  # Determine direction
            next_position = (current_x + step_x, current_y)
        else:  # Prioritize vertical movement
            step_y = 1 if move_y > 0 else -1
            next_position = (current_x, current_y + step_y)
        self.model.grid.move_agent(self, next_position)

        # Attempt to move to the next position
        '''if not self.model.move_robot(self, next_position):  # If move not successful
            # Try the secondary move if the primary move is blocked
            if abs(move_x) <= abs(move_y):  # Secondary move is horizontal
                step_x = 1 if move_x > 0 else -1
                secondary_position = (current_x + step_x, current_y)
            else:  # Secondary move is vertical
                step_y = 1 if move_y > 0 else -1
                secondary_position = (current_x, current_y + step_y)
            
            self.model.move_robot(self, secondary_position)  # Attempt secondary move'''
        
    def move_to_least_visited(self):
        neighbors = self.model.grid.get_neighborhood(self.pos, moore=False, include_center=False)
        allowed_neighbors = [pos for pos in neighbors if self.model.is_position_allowed(self, pos)]
        # Choose the neighbor with the least pheromones
        next_move = min(allowed_neighbors, key=lambda pos: (self.model.pheromone_levels['yellow'][pos], random.random()))
        return next_move

    def deposit_pheromone(self):
        x, y = self.pos
        self.model.pheromone_levels['yellow'][(x, y)] += 1  # Only update yellow pheromone levels

    def do(self, action):
        """Perform an action and update the environment and knowledge accordingly."""
        if action == "collect_waste" or action == "transform_waste":
            self.model.perform_action(self, action)
        elif action[0] == "move_to_location":
            self.model.move_agent_to_location(self, self.knowledge["yellow_waste_location"])
        elif action == "dispose_waste":
            # Assuming disposal location is known and is self.pos
            self.model.perform_action(self, action)
            waste_location = self.pos
            message_content = {"waste_type": "red", "location": waste_location}
            message = Message(from_agent=self.get_name(), to_agent="RedRobot", message_performative=MessagePerformative.INFORM_REF, content=message_content)
            self.message_service.store_message(message)
        elif action == "move_randomly":
            new_position = self.move_to_least_visited()
            self.model.move_robot(self, new_position)
            self.deposit_pheromone()


    def step(self):
        messages = self.get_new_messages()
        for msg in messages:
            if msg.get_performative() == MessagePerformative.INFORM_REF:
                # Handle messages specifying waste locations
                # Assume content is in the format {"waste_type": "yellow", "location": (x, y)}
                content = msg.get_content()
                if content["waste_type"] == "yellow":
                    # Add location to knowledge base
                    self.knowledge["yellow_waste_location"] = content["location"]
                    print(f"Received waste location: {self.knowledge['yellow_waste_location']}")
        percepts = self.percepts()
        action = self.deliberate(self.knowledge)
        self.do(action)
        if self.pos == self.knowledge.get("yellow_waste_location"):
            self.knowledge['task_completed'] = True
            print(f"{self.get_name()} has reached the destination and completed the task.")
            self.knowledge["yellow_waste_location"] =  None  # Clear the location from knowledge

class RedRobot(CommunicatingAgent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model, name=f"RedRobot")
        self.knowledge = {"collected_waste": [], "waste_here": False, "current_position": None, "red_waste_location": None}

    def percepts(self):
        """Gather information from the environment."""
        contents = self.model.grid.get_cell_list_contents([self.pos])
        waste_here = any(isinstance(c, Waste) and c.waste_type == "red" for c in contents)
        self.knowledge.update({"waste_here": waste_here, "current_position": self.pos})

    def deliberate(self, knowledge):
        """Decide on an action based on the current knowledge."""
        if self.knowledge.get("red_waste_location"):
            target_location = self.knowledge["red_waste_location"]
            if self.pos == target_location and knowledge["waste_here"]:
                if len(knowledge["collected_waste"]) == 0:
                    return "collect_waste"
                return "dispose_waste"
            else:
                return "move_to_location", target_location
        elif knowledge["waste_here"] and len(knowledge["collected_waste"]) == 0:
            return "collect_waste" 
        elif len(knowledge["collected_waste"]) == 1:
            return "dispose_waste"
        # Otherwise, move randomly.
        else:
            return "move_randomly"
        
    def move_to_least_visited(self):
        neighbors = self.model.grid.get_neighborhood(self.pos, moore=False, include_center=False)
        # Choose the neighbor with the least pheromones
        next_move = min(neighbors, key=lambda pos: (self.model.pheromone_levels['red'][pos], random.random()))
        return next_move

    def deposit_pheromone(self):
        x, y = self.pos
        self.model.pheromone_levels['red'][(x, y)] += 1  # Only update red pheromone levels

    def do(self, action):
        """Perform an action and update the environment and knowledge accordingly."""
        if action == "collect_waste" or action == "dispose_waste" :
            self.model.perform_action(self, action)
        elif action[0] == "move_to_location":
            self.model.move_agent_to_location(self, self.knowledge["red_waste_location"])
        elif action == "move_randomly":
            new_position = self.move_to_least_visited()
            self.model.move_robot(self, new_position)
            self.deposit_pheromone()

    def step(self):
        messages = self.get_new_messages()
        for msg in messages:
            if msg.get_performative() == MessagePerformative.INFORM_REF:
                # Handle messages specifying waste locations
                # Assume content is in the format {"waste_type": "yellow", "location": (x, y)}
                content = msg.get_content()
                if content["waste_type"] == "red":
                    # Add location to knowledge base
                    self.knowledge["red_waste_location"] = content["location"]
                    print(f"Received waste location: {self.knowledge['red_waste_location']}")
        percepts = self.percepts()
        action = self.deliberate(self.knowledge)
        self.do(action)
        if self.pos == self.knowledge.get("red_waste_location"):
            self.knowledge['task_completed'] = True
            print(f"{self.get_name()} has reached the destination and completed the task.")
            self.knowledge["red_waste_location"] =  None  # Clear the location from knowledge

#FIXED

