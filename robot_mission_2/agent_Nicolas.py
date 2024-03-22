from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid

class V0Agent(Agent):
    """ An agent with no waste"""
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.waste = 0

    def move(self):
        possible_positions = self.model.grid.get_neighborhood(
            self.pos)
            #moore=True,
            #include_center=False)
        new_position = self.random.choice(possible_positions)
        self.model.grid.move_agent(self, new_position)

    def transform(self): 
        transformed = 0
        if self.waste ==1 : 
            transformed =+1 
            self.waste = self.waste - 1

    def give_money(self):
        cellmates = self.model.grid.get_cell_list_contents([self.pos])
        if len(cellmates) > 1:
            other = self.random.choice(cellmates)
            other.wealth += 1
            self.wealth -= 1

    def step(self):
        self.move()
        if self.wealth > 0:
            self.give_money()