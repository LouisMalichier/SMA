#Group n°2
#22/03/2024
#Members : Badard Alexis, Malichier Louis, Saudreau Nicolas, Maamar Marouane

from mesa import Model
from mesa.space import MultiGrid
from mesa.time import RandomActivation
from agents import GreenRobot, YellowRobot, RedRobot  # Ensure this import matches your project structure
from objects import Waste , WasteDisposalZone, Radioactivity 
import random

class RobotMission(Model):
    def __init__(self, width, height, initial_green_waste, initial_yellow_waste, initial_red_waste):
        super().__init__() 
        self.grid = MultiGrid(width, height, False)
        self.schedule = RandomActivation(self)
        self.initial_green_waste = initial_green_waste
        self.initial_yellow_waste = initial_yellow_waste
        self.initial_red_waste = initial_red_waste

        l = self.grid.width // 3  # Divide the grid width by 3 to get the width of each zone
        for x in range(self.grid.width):
            for y in range(self.grid.height):
                # Zone assignment based on x coordinate
                if x <= l:
                    zone = "z1"
                elif x <= 2 * l:
                    zone = "z2"
                else:  # x > 2 * l
                    zone = "z3"
                # No need to call self.assign_radioactivity_level here as Radioactivity's __init__ does that
                radioactivity_agent = Radioactivity(self.schedule.get_agent_count(), self, zone)
                self.grid.place_agent(radioactivity_agent, (x, y))
                
        # Initialize robots within their respective zones
        z_width = l  # Width of zones z1, z2 and z3
        height = self.grid.height

        # Function to find an empty cell within specified bounds
        def find_empty_cell(x_start, x_end, height, grid):
            while True:
                x = random.randrange(x_start, x_end)
                y = random.randrange(0, height)
                if grid.is_cell_empty((x, y)):
                    return x, y

        # Place Green Robots in zone z1
        for _ in range(1):  # Adjust numbers as needed
            x, y = find_empty_cell(0, z_width, height, self.grid)
            robot = GreenRobot(self.schedule.get_agent_count(), self)
            self.schedule.add(robot)
            self.grid.place_agent(robot, (x, y))

        # Place Yellow Robots, which can start in z1 or z2, for simplicity here we allow the entire range except z3
        for _ in range(1):  # Adjust numbers as needed
            x, y = find_empty_cell(0, 2 * z_width, height, self.grid)  # Adjust the range for yellow robots
            robot = YellowRobot(self.schedule.get_agent_count(), self)
            self.schedule.add(robot)
            self.grid.place_agent(robot, (x, y))

        # Place Red Robots anywhere in the grid
        for _ in range(1):  # Adjust numbers as needed
            x, y = find_empty_cell(0, self.grid.width, height, self.grid)
            robot = RedRobot(self.schedule.get_agent_count(), self)
            self.schedule.add(robot)
            self.grid.place_agent(robot, (x, y))
        
        # Randomly placing initial wastes
        for _ in range(initial_green_waste):
            self.place_waste_in_zone("green", 0, z_width , height)
        for _ in range(initial_yellow_waste):
            self.place_waste_in_zone("yellow", z_width, 2 * z_width , height)
        for _ in range(initial_red_waste):
            self.place_waste_in_zone("red", 2 * z_width , width - 1, height)

        # Define disposal zones at the far east of each zone
        for y in range(height):
            # Place a WasteDisposalZone agent at the last column of z1
            dz1_pos = (z_width , y)
            dz1_agent = WasteDisposalZone(self.schedule.get_agent_count(), self)
            self.grid.place_agent(dz1_agent, dz1_pos)
            self.schedule.add(dz1_agent)

            # Place a WasteDisposalZone agent at the last column of z2
            dz2_pos = (2 * z_width , y)
            dz2_agent = WasteDisposalZone(self.schedule.get_agent_count(), self)
            self.grid.place_agent(dz2_agent, dz2_pos)
            self.schedule.add(dz2_agent)

            # Place a WasteDisposalZone agent at the last column of the entire grid (z3)
            dz3_pos = (self.grid.width , y)  # Ensure this is the correct position for z3's disposal zone
            dz3_agent = WasteDisposalZone(self.schedule.get_agent_count(), self)
            self.grid.place_agent(dz3_agent, dz3_pos)
            self.schedule.add(dz3_agent)

    def place_waste_in_zone(self, waste_type, x_start, x_end, height):
        waste = Waste(self.schedule.get_agent_count(), self, waste_type=waste_type)
        while True:
            pos = (random.randrange(x_start, x_end), random.randrange(height))
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
            # Each robot type can only collect a specific type of waste
            target_waste_type = "green" if isinstance(agent, GreenRobot) else ("yellow" if isinstance(agent, YellowRobot) else "red")
            for content in contents:
                if isinstance(content, Waste) and content.waste_type == target_waste_type and len(agent.knowledge["collected_waste"]) < 2:
                    agent.knowledge["collected_waste"].append(content)
                    self.grid.remove_agent(content)
                    break  
        elif action == "transform_waste":
            if isinstance(agent, GreenRobot) and len(agent.knowledge["collected_waste"]) == 2:
                yellow_waste = Waste(self.schedule.get_agent_count(), self, waste_type="yellow")
                self.schedule.add(yellow_waste)
                agent.knowledge["collected_waste"][0] = yellow_waste
                agent.knowledge["collected_waste"] = agent.knowledge["collected_waste"][:1]
                print(agent.knowledge["collected_waste"])
            if isinstance(agent, YellowRobot) and len(agent.knowledge["collected_waste"]) == 2:
                red_waste = Waste(self.schedule.get_agent_count(), self, waste_type="red")
                self.schedule.add(red_waste)
                agent.knowledge["collected_waste"][0] = red_waste
                agent.knowledge["collected_waste"] = agent.knowledge["collected_waste"][:1]
                print(agent.knowledge["collected_waste"])
            """Model processes the action requested by the agent."""
        elif action == "dispose_waste":
            # Dynamically determine the waste type each robot disposes of
            disposal_waste_type = {"GreenRobot": "yellow", "YellowRobot": "red", "RedRobot": "red"}[type(agent).__name__]

            # Check if the agent is at its disposal zone
            if self.is_in_disposal_zone(agent):
                # Go through the collected waste
                for waste in list(agent.knowledge["collected_waste"]):  # Use list() to clone since we're modifying inside loop
                    if waste.waste_type == disposal_waste_type:
                        # Remove the disposed waste from the robot's knowledge
                        agent.knowledge["collected_waste"].remove(waste)
                        if disposal_waste_type == "red":
                            # For RedRobot, remove the waste from the grid
                            self.grid.remove_agent(waste)
                        else :
                            self.grid.place_agent(waste, self.disposal_zone)
                        print(agent.knowledge["collected_waste"])
                        break  # Assuming we only dispose of one waste at a time                               
            else:
                # Move towards disposal zone
                self.move_agent_towards_disposal_zone(agent)

    def move_robot(self, robot, new_position):
        # Check if new_position is within the robot's allowed zone
        if not self.is_position_allowed(robot, new_position):
            return  # If not allowed, don't move the robot

        # Check if the cell is occupied by another robot
        contents = self.grid.get_cell_list_contents(new_position)
        if any(isinstance(c, (GreenRobot, YellowRobot, RedRobot)) for c in contents):
            return  # If occupied, don't move the robot

        # Move the robot to new_position
        self.grid.move_agent(robot, new_position)

    def is_position_allowed(self, robot, position):
        # Retrieve all agents at the target position
        contents = self.grid.get_cell_list_contents(position)
        # Filter for Radioactivity agents
        radioactivity_agents = [agent for agent in contents if isinstance(agent, Radioactivity)]
        # If there are no radioactivity agents at the position, consider the move not allowed by default
        if not radioactivity_agents:
            return False
        # A single Radioactivity agent per cell
        zone = radioactivity_agents[0].zone      
        # Determine if the robot is allowed based on its type and the zone
        if isinstance(robot, GreenRobot) and zone == "z1":
            return True
        elif isinstance(robot, YellowRobot) and (zone == "z1" or zone == "z2"):
            return True
        elif isinstance(robot, RedRobot):
            # Assuming RedRobots can move in any zone
            return True        
        # If none of the above conditions are met, the position is not allowed
        return False
    
    def move_agent_towards_disposal_zone(self, agent):
        """Move the agent one step towards its disposal zone."""
        x, y = agent.pos

        # Determine the disposal zone x-coordinate (dx) based on the robot type
        z_width = self.grid.width // 3
        if isinstance(agent, GreenRobot):
            dx = z_width   # Disposal zone for GreenRobot is at the end of z1
        elif isinstance(agent, YellowRobot):
            dx = 2 * z_width  # Disposal zone for YellowRobot is at the end of z2
        elif isinstance(agent, RedRobot):
            dx = self.grid.width   # Disposal zone for RedRobot is at the end of the grid (z3)

        # Move horizontally towards dx
        if x < dx:
            new_x = x + 1
        elif x > dx:
            new_x = x - 1
        else:
            new_x = x

        # For this scenario, we assume the disposal zone spans the entire height of the zone,
        # so the robot does not need to move vertically to find it.
        new_y = y

        # Check if the new position is allowed and not occupied by another robot
        new_position = (new_x, new_y)
        if self.is_position_allowed(agent, new_position):
            contents = self.grid.get_cell_list_contents(new_position)
            if not any(isinstance(c, (GreenRobot, YellowRobot, RedRobot)) for c in contents):
                # Move the agent to the new position if it's empty
                self.grid.move_agent(agent, new_position)


        
