from mesa import Model
from mesa.space import MultiGrid
from mesa.time import RandomActivation
from agents import GreenRobot  # Ensure this import matches your project structure
from objects import Waste, WasteDisposalZone
import random

class MultiZoneRobotMission(Model):
    def __init__(self, width=9, height=3, initial_waste=4):
        super().__init__()
        self.zone_width = 3  # Width of each zone
        self.grid = MultiGrid(width+3, height, False)
        self.schedule = RandomActivation(self)

        # Initialize three disposal zones, one for each zone
        def generate_disposal_zones(nbr_zones=3):
            disposal_zones = []
            for i in range(nbr_zones):
                x = (i + 1) * 3 + i
                for y in range(3):
                    disposal_zones.append((x, y))
            return disposal_zones

        self.disposal_zones = generate_disposal_zones()
        for disposal_zone in self.disposal_zones:
            disposal_zone_agent = WasteDisposalZone(self.schedule.get_agent_count(), self)
            self.grid.place_agent(disposal_zone_agent, disposal_zone)
            self.schedule.add(disposal_zone_agent)

        # Initialize robots and waste for each zone
        for zone_num, disposal_zone in enumerate( [(2, 1), (5, 1), (8, 1)]):
            self.initialize_zone(zone_num, disposal_zone, initial_waste)

    def initialize_zone(self, zone_num, disposal_zone, initial_waste):
        zone_offset = zone_num * (self.zone_width + 1)  # Offset for placing agents in each zone
        # Initialize a Green Robot at a random position in the zone
        robot = GreenRobot(self.schedule.get_agent_count(), self)
        self.schedule.add(robot)
        robot_pos = (random.randrange(self.zone_width) + zone_offset, random.randrange(self.grid.height))
        self.grid.place_agent(robot, robot_pos)

        # Randomly place initial green waste in the zone
        for _ in range(initial_waste):
            waste = Waste(self.schedule.get_agent_count(), self, waste_type="green")
            while True:
                # Ensure the generated position is within the bounds of the zone
                pos = (random.randrange(self.zone_width) + zone_offset, random.randrange(self.grid.height))
                if self.grid.is_cell_empty(pos):
                    self.grid.place_agent(waste, pos)
                    self.schedule.add(waste)
                    break


    def step(self):
        self.schedule.step()

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
            # Check if the agent is at any of the disposal zones
            if agent.pos in self.disposal_zones:
                # Go through the collected waste to find a yellow one to dispose of
                for waste in agent.knowledge["collected_waste"]:
                    if waste.waste_type == "yellow":
                        # Remove the disposed waste from the robot's knowledge
                        agent.knowledge["collected_waste"].remove(waste)
                        # Find the index of the disposal zone where the agent is located
                        disposal_zone_index = self.disposal_zones.index(agent.pos)
                        # Calculate the corresponding offset to find the correct zone
                        zone_offset = disposal_zone_index * (self.zone_width + 1)
                        # Create a new yellow Waste agent in the disposal zone
                        #self.grid.place_agent(waste, (random.randrange(self.zone_width) + zone_offset, random.randrange(self.grid.height))) # PROBLEME
                        print(agent.knowledge["collected_waste"])
                        break  # Assuming we only dispose of one waste at a time
            else:
                # Move towards disposal zone
                self.move_agent_towards_disposal_zone(agent)

    def move_agent_towards_disposal_zone(self, agent):
        """Move the agent one step towards the disposal zone."""
        current_x, current_y = agent.pos
        # Find the nearest disposal zone
        nearest_disposal_zone = min(self.disposal_zones, key=lambda x: abs(x[0] - current_x))
        dx, dy = nearest_disposal_zone
        # Move horizontally towards dx
        if current_x < dx:
            new_x = current_x + 1
        elif current_x > dx:
            new_x = current_x - 1
        else:
            new_x = current_x
        # Move vertically towards dy
        if current_y < dy:
            new_y = current_y + 1
        elif current_y > dy:
            new_y = current_y - 1
        else:
            new_y = current_y
        # Update the agent's position
        agent.model.grid.move_agent(agent, (new_x, new_y))