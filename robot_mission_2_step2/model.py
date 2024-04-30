#Group n°2
#22/03/2024
#Members : Badard Alexis, Malichier Louis, Saudreau Nicolas, Maamar Marouane

from mesa import Model, DataCollector
from mesa.space import MultiGrid
from mesa.time import RandomActivation
from agents import GreenRobot, YellowRobot, RedRobot  
from objects import Waste , WasteDisposalZone, Radioactivity 
from schedule import RandomActivationScheduler
from communication.message.MessageService import MessageService
import random

class RobotMission(Model):
    def __init__(self, width, height, initial_green_waste, initial_yellow_waste, initial_red_waste, nb_yellow_agent, nb_green_agent, nb_red_agent):
        super().__init__() 
        self.__messages_service = MessageService(self.schedule)
        self.grid = MultiGrid(width, height, torus = False)
        self.pheromone_levels = {
            'green': {(x, y): 0 for x in range(width) for y in range(height)},
            'yellow': {(x, y): 0 for x in range(width) for y in range(height)},
            'red': {(x, y): 0 for x in range(width) for y in range(height)}
        }
        self.pheromone_decay_rate = 0.3  # 30% decay rate per step so as to not have pheromones last forever
        self.schedule = RandomActivationScheduler(self)
        self.initial_green_waste = initial_green_waste
        self.initial_yellow_waste = initial_yellow_waste
        self.initial_red_waste = initial_red_waste
        self.nb_yellow_agent = nb_yellow_agent
        self.nb_green_agent = nb_green_agent
        self.nb_red_agent = nb_red_agent

        l = self.grid.width // 3  # Divide the grid width by 3 to get the width of each zone
        for x in range(self.grid.width):
            for y in range(self.grid.height):
                # Zone assignment based on x coordinate
                if x < l:
                    zone = "z1"
                elif l <= x < 2 * l:
                    zone = "z2"
                else:  # x > 2 * l
                    zone = "z3"
                # No need to call self.assign_radioactivity_level here as Radioactivity's __init__ does that
                radioactivity_agent = Radioactivity(self.schedule.get_agent_count(), self, zone)
                self.grid.place_agent(radioactivity_agent, (x, y))
                self.schedule.add(radioactivity_agent)
                
        # Initialize robots within their respective zones
        z_width = l  # Width of zones z1, z2 and z3
        height = self.grid.height
        self.datacollector = DataCollector({
                "Waste": lambda m: m.schedule.get_type_count(Waste),
            }
                )

        # Function to find an empty cell within specified bounds
        def find_empty_cell(x_start, x_end, height, grid):
            while True:
                x = random.randrange(x_start, x_end)
                y = random.randrange(0, height)
                # Get all agents in the chosen cell
                cell_contents = grid.get_cell_list_contents((x, y))
                # Check if any agents in the cell are robots
                if not any(isinstance(agent, (GreenRobot, YellowRobot, RedRobot)) for agent in cell_contents):
                    return x, y


        # Place Green Robots in zone z1
        for _ in range(self.nb_green_agent):  # Adjust numbers as needed
            x, y = find_empty_cell(0, z_width - 1, height, self.grid)
            robot = GreenRobot(self.schedule.get_agent_count(), self)
            self.schedule.add(robot)
            self.grid.place_agent(robot, (x, y))
           

        # Place Yellow Robots, which can start in z1 or z2, for simplicity here we allow the entire range except z3
        for _ in range(self.nb_yellow_agent):  # Adjust numbers as needed
            x, y = find_empty_cell(0, 2 * z_width - 1, height, self.grid)  # Adjust the range for yellow robots
            robot = YellowRobot(self.schedule.get_agent_count(), self)
            self.schedule.add(robot)
            self.grid.place_agent(robot, (x, y))
          

        # Place Red Robots anywhere in the grid
        for _ in range(self.nb_red_agent):  # Adjust numbers as needed
            x, y = find_empty_cell(0, self.grid.width - 1, height, self.grid)
            robot = RedRobot(self.schedule.get_agent_count(), self)
            self.schedule.add(robot)
            self.grid.place_agent(robot, (x, y))
            
        
        # Randomly placing initial wastes
        for _ in range(initial_green_waste):
            self.place_waste_in_zone("green", 0, z_width - 1 , height)
            
        for _ in range(initial_yellow_waste):
            self.place_waste_in_zone("yellow", z_width, 2 * z_width - 1, height)
            
        for _ in range(initial_red_waste):
            self.place_waste_in_zone("red", 2 * z_width , width - 1, height)
            

        # Define disposal zones at the far east of each zone
        for y in range(height):
            # Place a WasteDisposalZone agent at the last column of z1
            dz1_pos = (z_width - 1 , y)
            dz1_agent = WasteDisposalZone(self.schedule.get_agent_count(), self)
            self.grid.place_agent(dz1_agent, dz1_pos)
            self.schedule.add(dz1_agent)

            # Place a WasteDisposalZone agent at the last column of z2
            dz2_pos = (2 * z_width - 1 , y)
            dz2_agent = WasteDisposalZone(self.schedule.get_agent_count(), self)
            self.grid.place_agent(dz2_agent, dz2_pos)
            self.schedule.add(dz2_agent)

            # Place a WasteDisposalZone agent at the last column of the entire grid (z3)
            dz3_pos = (self.grid.width - 1 , y)  # Ensure this is the correct position for z3's disposal zone
            dz3_agent = WasteDisposalZone(self.schedule.get_agent_count(), self)
            self.grid.place_agent(dz3_agent, dz3_pos)
            self.schedule.add(dz3_agent)

    def dispatch_messages_conditionally(self):
        """Dispatch messages stored in MessageService based on specific conditions."""
        all_messages = self.__messages_service.retrieve_all_messages()

        for message in all_messages:
            # Filter agents by type indicated in the message destination
            agent_type = message.get_dest()
            eligible_agents = [agent for agent in self.schedule.agents if isinstance(agent, eval(agent_type))]

            # Process eligible agents to find the one with minimum waste who hasn't completed the task
            if eligible_agents:
                filtered_agents = [agent for agent in eligible_agents if not agent.knowledge.get('task_completed')]
                if filtered_agents:
                    min_waste = min(len(agent.knowledge['collected_waste']) for agent in filtered_agents)
                    candidates = [agent for agent in filtered_agents if len(agent.knowledge['collected_waste']) == min_waste]

                    # Select randomly from candidates if there's a tie
                    if candidates:
                        selected_agent = random.choice(candidates)
                        selected_agent.receive_message(message)
                        print(f"Dispatched message to {selected_agent.get_name()} based on waste criteria.")
                    else:
                        print("No eligible agents need the message.")
                else:
                    print("All agents have completed the task.")

    def print_zones(self):
        print("Current zone types by cell:")
        for x in range(self.grid.width):
            for y in range(self.grid.height):
                cell_contents = self.grid.get_cell_list_contents((x, y))
                # Find Radioactivity agent in the cell to get the zone type
                radioactivity_agent = next((agent for agent in cell_contents if isinstance(agent, Radioactivity)), None)
                if radioactivity_agent is not None:
                    print(f"Cell ({x}, {y}) is in zone {radioactivity_agent.zone}")
    def decay_pheromones(self):
            for (x, y), level in self.pheromone_levels['green'].items():
                self.pheromone_levels['green'][(x, y)] = max(level - self.pheromone_decay_rate, 0)
            # Repeat for other pheromone types if necessary
            for (x, y), level in self.pheromone_levels['yellow'].items():
                self.pheromone_levels['yellow'][(x, y)] = max(level - self.pheromone_decay_rate, 0)
            for (x, y), level in self.pheromone_levels['red'].items():
                self.pheromone_levels['red'][(x, y)] = max(level - self.pheromone_decay_rate, 0)

    def step(self):
        self.schedule.step()
        self.dispatch_messages_conditionally()  # Dispatch messages after all agents have stepped
        self.datacollector.collect(self)
        self.decay_pheromones()

    def place_waste_in_zone(self, waste_type, x_start, x_end, height):
        waste = Waste(self.schedule.get_agent_count(), self, waste_type=waste_type)
        while True:
            pos = (random.randrange(x_start, x_end), random.randrange(height))
            self.grid.place_agent(waste, pos)
            self.schedule.add(waste)
            break

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
                    self.schedule.remove(content)
                    print(agent ,agent.knowledge["collected_waste"])
                    break  
        elif action == "transform_waste":
            if isinstance(agent, GreenRobot) and len(agent.knowledge["collected_waste"]) == 2:
                agent.knowledge["collected_waste"].clear()
                yellow_waste = Waste(self.schedule.get_agent_count(), self, waste_type="yellow")
                self.schedule.add(yellow_waste)
                agent.knowledge["collected_waste"].append(yellow_waste)
                print(agent, agent.knowledge["collected_waste"])
            if isinstance(agent, YellowRobot) and len(agent.knowledge["collected_waste"]) == 2:
                agent.knowledge["collected_waste"].clear()
                red_waste = Waste(self.schedule.get_agent_count(), self, waste_type="red")
                self.schedule.add(red_waste)
                agent.knowledge["collected_waste"].append(red_waste)
                print(agent , agent.knowledge["collected_waste"])
            """Model processes the action requested by the agent."""
        elif action == "dispose_waste":
            # Check if the agent is in its disposal zone
            if not self.is_in_disposal_zone(agent):
                # If not, move towards the disposal zone (this logic must be implemented)
                self.move_agent_towards_disposal_zone(agent)

            else :
                # GreenRobot logic: dispose of yellow waste
                if isinstance(agent, GreenRobot):
                    for waste in agent.knowledge["collected_waste"]:
                        #yellow_waste = Waste(self.schedule.get_agent_count(), self, waste_type="yellow")
                        self.grid.place_agent(waste, agent.pos)
                        #self.schedule.add(yellow_waste)
                        agent.knowledge["collected_waste"].clear()
                        print(agent, agent.knowledge["collected_waste"])
                        
                
                # YellowRobot logic: dispose of red waste
                elif isinstance(agent, YellowRobot): 
                    # Convert to red waste and place in disposal zone
                    for waste in agent.knowledge["collected_waste"]:
                        #red_waste = Waste(self.schedule.get_agent_count(), self, waste_type="red")
                        self.grid.place_agent(waste, agent.pos)
                        #self.schedule.add(red_waste)
                        agent.knowledge["collected_waste"].clear()
                        print(agent, agent.knowledge["collected_waste"])
                        

                # RedRobot logic: Simply disposes of red waste
                elif isinstance(agent, RedRobot):
                    agent.knowledge["collected_waste"].clear()   
                        #self.grid.remove_agent(waste)
                    print(agent, agent.knowledge["collected_waste"])
                        

    def is_in_disposal_zone(self, agent):
        # Determine the disposal zone x-coordinate (dx) based on the robot type
        z_width = self.grid.width // 3
        if isinstance(agent, GreenRobot):
            dx = z_width - 1   # Disposal zone for GreenRobot is at the end of z1
        elif isinstance(agent, YellowRobot):
            dx = 2 * z_width - 1
        elif isinstance(agent, RedRobot):
            dx = self.grid.width - 1
        # Check if the agent is at the disposal zone
        return agent.pos[0] == dx
    

    def move_robot(self, robot, new_position):
        # Check if new_position is within the robot's allowed zone
        if not self.is_position_allowed(robot, new_position):
            print(f"Move not allowed for {robot.unique_id} to {new_position}")
            return  # If not allowed, don't move the robot

        # Check if the cell is occupied by another robot
        contents = self.grid.get_cell_list_contents(new_position)
        if any(isinstance(c, (GreenRobot, YellowRobot, RedRobot)) for c in contents):
            print(f"Cell {new_position} is occupied")
            return  # If occupied, don't move the robot

        # Move the robot to new_position
        self.grid.move_agent(robot, new_position)

    def is_position_allowed(self, robot, position):
        radioactivity_agents = []
        # Retrieve all agents at the target position
        contents = self.grid.get_cell_list_contents(position)
        # Filter for Radioactivity agents
        radioactivity_agents = [agent for agent in contents if isinstance(agent, Radioactivity)]
        #print(f"Contents at {position}: {contents}")
        # If there are no radioactivity agents at the position, consider the move not allowed by default
        if not radioactivity_agents:
            print("No radioactivity agent at position")
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
        print(f"Move not allowed for {type(robot).__name__} to zone {zone}")
        return False
    
    def move_agent_to_location(self, agent, target_location):
        """Move the agent one step towards a specified location."""
        current_x, current_y = agent.pos
        target_x, target_y = target_location

        # Decide whether to move in x or y direction
        if current_x != target_x:
            step_x = 1 if target_x > current_x else -1
            new_x = current_x + step_x
        else:
            new_x = current_x

        if current_y != target_y:
            step_y = 1 if target_y > current_y else -1
            new_y = current_y + step_y
        else:
            new_y = current_y

        # Prioritize x movement if both x and y need to change
        if new_x != current_x:
            new_position = (new_x, current_y)
        else:
            new_position = (current_x, new_y)

        # Check if the new position is allowed and not occupied by another robot
        if self.is_position_allowed(agent, new_position):
            contents = self.grid.get_cell_list_contents(new_position)
            if not any(isinstance(c, (GreenRobot, YellowRobot, RedRobot)) for c in contents):
                # Move the agent to the new position if it's empty
                self.grid.move_agent(agent, new_position)
            else:
                # If the first choice is blocked, check the second choice
                secondary_position = (current_x, new_y) if new_x != current_x else (new_x, current_y)
                if self.is_position_allowed(agent, secondary_position):
                    contents = self.grid.get_cell_list_contents(secondary_position)
                    if not any(isinstance(c, (GreenRobot, YellowRobot, RedRobot)) for c in contents):
                        self.grid.move_agent(agent, secondary_position)

    
    def move_agent_towards_disposal_zone(self, agent):
        """Move the agent one step towards its disposal zone."""
        x, y = agent.pos

        # Determine the disposal zone x-coordinate (dx) based on the robot type
        z_width = self.grid.width // 3
        if isinstance(agent, GreenRobot):
            dx = z_width - 1   # Disposal zone for GreenRobot is at the end of z1
        elif isinstance(agent, YellowRobot):
            dx = 2 * z_width - 1 # Disposal zone for YellowRobot is at the end of z2
        elif isinstance(agent, RedRobot):
            dx = self.grid.width - 1  # Disposal zone for RedRobot is at the end of the grid (z3)

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


        
