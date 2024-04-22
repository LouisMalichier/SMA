#Group n°2
#22/03/2024
#Members : Badard Alexis, Malichier Louis, Saudreau Nicolas, Maamar Marouane

from mesa import Agent
import model
import random

class Radioactivity(Agent):
    """A non-behavioral agent representing the level of radioactivity in a zone."""
    def __init__(self, unique_id, model, zone):
        super().__init__(unique_id, model)
        self.zone = zone
        self.radioactivity = self.assign_radioactivity_level(zone)
        
    def assign_radioactivity_level(self, zone):
        if zone == "z1":
            return random.uniform(0, 0.33)
        elif zone == "z2":
            return random.uniform(0.33, 0.66)
        else:  # zone "z3"
            return random.uniform(0.66, 1)

class WasteDisposalZone(Agent):
    """A non-behavioral agent indicating the waste disposal zone."""
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        # Assuming a value to identify this as a disposal zone, if needed.
        self.is_disposal_zone = True

class Waste(Agent):
    """Represents waste objects."""
    def __init__(self, unique_id, model, waste_type):
        super().__init__(unique_id, model)
        self.waste_type = waste_type  # green, yellow, red

