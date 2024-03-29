#Group n°2
#22/03/2024
#Members : Badard Alexis, Malichier Louis, Saudreau Nicolas, Maamar Marouane

from mesa.time import BaseScheduler
import random

class CustomScheduler(BaseScheduler):
    """A scheduler that activates each agent once per step, in random order, without regard to type."""
    def step(self):
        for agent in self.agent_buffer(shuffled=True):
            agent.step()
        self.steps += 1
        self.time += 1

