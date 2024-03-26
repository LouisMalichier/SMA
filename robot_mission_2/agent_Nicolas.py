from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid

class Waste(Agent):
    def __init__(self, unique_id, pos, color ,model):
        super().__init__(unique_id, model)
        self.color = color


class Robot(Agent):
    """ An agent with no waste"""
    def __init__(self, unique_id, pos, color, model):
        super().__init__(unique_id, model)
        self.inventory = []
        self.robot_type=color

    def V0move(self):
        possible_positions = self.model.grid.get_neighborhood(
            self.pos,
            moore=False,
            include_center=False )
        new_position = self.random.choice(possible_positions)
        self.model.grid.move_agent(self, new_position)

    def V0step(self):
            self.move()
            cellmates = self.model.grid.get_cell_list_contents([self.pos])
            waste = [obj for obj in cellmates if isinstance(obj, Waste)]
            if waste:
                target = waste[0]
                self.inventory.append(target)
                self.model.grid.remove_agent(target)
                self.model.schedule.remove(target)


    def step(self):
        if self.robot_type == "Green":
            def move(self):
                #Espace disponible pour le robot 
                green_zone = self.model.green_zone

                #Définir tous les voisins
                all_possible = self.model.grid.get_neighborhood(
                self.pos,
                moore=False,
                include_center=False )

                #ATTENTION : Il faut ajouter le cas où le robot est plein (cad quand 1 yellow waste dans l'inventory) et se dirige vers l'est !

                #Ne conserver que les voisins qui sont dans la zone acceptée
                possible_positions = []
                for position in all_possible :
                    if position in green_zone : possible_positions.append(position)

                new_position = self.random.choice(possible_positions)
                self.model.grid.move_agent(self, new_position)

            #etape 1 : bouger   
            move(self)

            #etape 2 : Comprendre ce qu'il y a dans la case où l'on vient d'arriver 
            cellmates = self.model.grid.get_cell_list_contents([self.pos])
            waste = [obj for obj in cellmates if isinstance(obj, Waste)]

            #etape 3 : analyser le possible waste de la case 
            if waste:
                target = waste[0]
                self.inventory.append(target)
                self.model.grid.remove_agent(target)
                self.model.schedule.remove(target)

            if len(self.inventory) < 2:
                self.pick_up_waste()
            else:
                self.transform_waste()
        elif self.robot_type == "Yellow":
            if len(self.inventory) < 2:
                self.pick_up_waste()
            else:
                self.transform_waste()
        elif self.robot_type == "Red":
            if len(self.inventory) < 1:
                self.pick_up_waste()
            else:
                self.transport_waste()

    '''''

    def transform(self): 
        transformed = 0
        if self.waste ==1 : 
            transformed =+1 
            self.waste = self.waste - 1
    '''
            
    


    '''
    def step(self):
        if self.robot_type == "Green":
            if len(self.inventory) < 2:
                self.pick_up_waste()
            else:
                self.transform_waste()
        elif self.robot_type == "Yellow":
            if len(self.inventory) < 2:
                self.pick_up_waste()
            else:
                self.transform_waste()
        elif self.robot_type == "Red":
            if len(self.inventory) < 1:
                self.pick_up_waste()
            else:
                self.transport_waste()
  

    def transport_waste(self):
        if self.robot_type == "Green":
            pass  # Green robots cannot transport waste
        elif self.robot_type == "Yellow":
            if len(self.inventory) >= 1 and self.model.grid.width > self.pos[0] + 1:
                self.inventory = []  # Consume 1 red waste
                self.move()
        elif self.robot_type == "Red":
            if len(self.inventory) >= 1 and self.model.grid.width > self.pos[0] + 1:
                self.inventory = []  # Consume 1 red waste
                self.move()
  '''

    # def give_money(self):
    #     cellmates = self.model.grid.get_cell_list_contents([self.pos])
    #     if len(cellmates) > 1:
    #         other = self.random.choice(cellmates)
    #         other.wealth += 1
    #         self.wealth -= 1

    # def step(self):
    #     self.move()
    #     if self.wealth > 0:
    #         self.give_money()


'''
class V0Waste(Agent):
    def __init__(self, unique_id, model, category, position):
        super().__init__(unique_id, model)
        self._category = None
        self.category = category
        self.position = position

    @property
    def category(self):
        return self._category
    
    @category.setter
    def category(self, value):
        if value not in ["green", "yellow", "red"]:  # Remplacez "value1", "value2", "value3" par les valeurs autorisées
            raise ValueError("Category must be one of ['green', 'yellow', 'red']")
        self._category = value

'''