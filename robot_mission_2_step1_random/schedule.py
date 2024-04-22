#Group n°2
#22/03/2024
#Members : Badard Alexis, Malichier Louis, Saudreau Nicolas, Maamar Marouane

from mesa.time import BaseScheduler, RandomActivationByType
from mesa import Agent
from typing import Callable, Optional, Type
import random

class CustomScheduler(BaseScheduler):
    """A scheduler that activates each agent once per step, in random order, without regard to type."""
    def step(self):
        for agent in self.agent_buffer(shuffled=True):
            agent.step()
        self.steps += 1
        self.time += 1

class RandomActivationScheduler(RandomActivationByType):

    def get_type_count(
        self,
        type_class: Type[Agent],
        filter_func: Optional[Callable[[Agent], bool]] = None,
    ) -> int:
        """
        Returns the current number of agents of certain type in the queue
        that satisfy the filter function.
        """
        if type_class not in self.agents_by_type:
            return 0
        count = 0
        for agent in self.agents_by_type[type_class].values():
            if filter_func is None or filter_func(agent):
                count += 1
        return count

