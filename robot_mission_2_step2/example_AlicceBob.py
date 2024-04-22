#!/usr/bin/env python3

import random

from mesa import Model
from mesa.time import RandomActivation

from communication.agent.CommunicatingAgent import CommunicatingAgent
from communication.message.Message import Message
from communication.message.MessagePerformative import MessagePerformative
from communication.message.MessageService import MessageService


class SpeakingAgent(CommunicatingAgent):
    """ """
    def __init__(self, unique_id, model, name, preferred_value):
        super().__init__(unique_id, model, name)
        self.preferred_value = preferred_value
        #self.__v = random.randint(0, 1000)

    def step(self):
        super().step()
        #To complete
        self.send_message(Message(self.get_name(), "Charles", MessagePerformative.QUERY_REF, "What is the value of v?"))
        print(f"{self.get_name()} asked Charles for the value of v")

        # Process the received messages and decide whether to ask for a change
        for msg in self.get_new_messages():
            if msg.get_content() != str(self.preferred_value):
                self.send_message(Message(self.get_name(), "Charles", MessagePerformative.PROPOSE, f"Please change v to {self.preferred_value}"))
                print(f"{self.get_name()} asked Charles to change v to {self.preferred_value}")

class CharlesAgent(CommunicatingAgent):
    def __init__(self, unique_id, model, name, v):
        super().__init__(unique_id, model, name)
        self.v = random.randint(0, 1000)

    def step(self):
        super().step()
        # Process all messages
        for msg in self.get_new_messages():
            if msg.get_performative() == MessagePerformative.QUERY_REF:
                # Send the current value of v
                
                self.send_message(Message(self.get_name(), msg.get_exp(), MessagePerformative.INFORM_REF, str(self.v)))
            elif msg.get_performative() == MessagePerformative.PROPOSE:
                # Change the value of v
                self.v = int(msg.get_content().split()[-1])
                print(f"{self.get_name()} changed v to {self.v}")

class SpeakingModel(Model):
    """ """
    def __init__(self):
        super().__init__()
        self.schedule = RandomActivation(self)
        self.__messages_service = MessageService(self.schedule)
        self.running = True

        # Create and add agents
        alice = SpeakingAgent("Alice", self, "Alice", preferred_value=10)
        bob = SpeakingAgent("Bob", self, "Bob", preferred_value=20)
        charles = CharlesAgent("Charles", self, "Charles", v=random.randint(0, 100))

        self.schedule.add(alice)
        self.schedule.add(bob)
        self.schedule.add(charles)

    def step(self):
        self.schedule.step()



if __name__ == "__main__":
    # Init the model and the agents
    speaking_model=SpeakingModel()

    # Launch the Communication part 
    step = 0
    while step < 10:
        speaking_model.step()
        step += 1
