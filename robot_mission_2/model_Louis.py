import mesa

from agent_Nicolas import Robot, Waste
from schedule import RandomActivationByTypeFiltered
import time

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
                "Robots": lambda m: m.schedule.get_type_count(Robot),
                "Waste": lambda m: m.schedule.get_type_count(Waste),
            }
        )

        #Create robot and waste if needed
        
        for i in range(self.initial_robot):
            x = self.random.randrange(self.width)
            y = self.random.randrange(self.height)
            robot = Robot(self.next_id(), (x, y), self) # Voir les paramètres de la class robot
            self.grid.place_agent(robot,(x, y))
            self.schedule.add(robot)

        for i in range(self.initial_waste):
            x = self.random.randrange(self.width)
            y = self.random.randrange(self.height)
            waste = Waste(self.next_id(), (x, y), self) # Voir les paramètres de la class robot
            self.grid.place_agent(waste,(x, y))
            self.schedule.add(waste)

        self.running = True
        self.datacollector.collect(self)

    def step(self):
        time.sleep(1)
        self.schedule.step()
        self.datacollector.collect(self)
        # self verbose if needed

        robot_positions = [agent.pos for agent in self.schedule.agents if isinstance(agent, Robot)]
        waste_positions = [agent.pos for agent in self.schedule.agents if isinstance(agent, Waste)]

        print("Positions des robots : ", robot_positions)
        print("Positions des déchets : ", waste_positions)

    def run_model(self):
        # Pas de self.step_count dans notre projet, mais plutot on continue de s'executer tant qu'il reste des dechets sur la grille, donc une condition en while sur waste

        dechet_etape_i=self.schedule.get_type_count(Waste)
        dechet_etape_iplus1=self.schedule.get_type_count(Waste)


        print(f'initial waste = {self.schedule.get_type_count(Waste)}')
        while self.schedule.get_type_count(Waste) != 0 : # Syntaxe à verifier mais exemple
            dechet_etape_i=self.schedule.get_type_count(Waste)
            self.step()
            dechet_etape_iplus1=self.schedule.get_type_count(Waste)
            if dechet_etape_iplus1 != dechet_etape_i : 
                print(f"Suppresion d'un déchet : il reste  {self.schedule.get_type_count(Waste)} dechets")

