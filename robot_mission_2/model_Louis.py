import mesa

from .agent_Nicolas import Robot, Waste
from .schedule import RandomActivationByTypeFiltered


class environment(mesa.Model):
    
    height = 3
    width = 3

    initial_robot = 1
    initial_waste = 4
    
    def __init__(
        self,
        width=3,
        height=3,
        initial_robot = 1,
        initial_waste = 4,
    ):
        super().__init__()
        self.width = width
        self.height = height
        self.initial_robot = initial_robot
        self.initial_waste = initial_waste
        
        self.schedule = RandomActivationByTypeFiltered(self)

        self.grid = mesa.space.MultiGrid(self.width, self.height, torus=True)
        self.datacollector = mesa.DataCollector(
            {
                "Wolves": lambda m: m.schedule.get_type_count(Robot),
                "Sheep": lambda m: m.schedule.get_type_count(Waste),
            }
        )

        #Create robot and waste if needed
        
        for i in range(self.initial_robot):
            x = self.random.randrange(self.width)
            y = self.random.randrange(self.height)
            robot = Robot() # Voir les paramètres de la class robot
            self.grid.place_agent(self.next_id(), (x, y), self)
            self.schedule.add(robot)

        for i in range(self.initial_waste):
            x = self.random.randrange(self.width)
            y = self.random.randrange(self.height)
            waste = Waste() # Voir les paramètres de la class robot
            self.grid.place_agent(self.next_id(), (x, y), self)
            self.schedule.add(waste)

        self.running = True
        self.datacollector.collect(self)

    def step(self):
        self.schedule.step()
        self.datacollector.collect(self)
        # self verbose if needed

    def run_model(self):
        # Pas de self.step_count dans notre projet, mais plutot on continue de s'executer tant qu'il reste des dechets sur la grille, donc une condition en while sur waste

        while self.schedule.get_type_count(Waste) != 0 : # Syntaxe à verifier mais exemple
            self.step()