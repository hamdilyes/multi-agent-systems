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
    def __init__(self, unique_id, model, name):
        super().__init__(unique_id, model, name)

    def step(self):
        super().step()
        list_message=self.get_new_messages()
        print(list_message)
        #To complete

class BrookerAgent(CommunicatingAgent):
    """ """
    def __init__(self, unique_id, model, name):
        super().__init__(unique_id, model, name)
        self.__v = random.randint(0, 1000)

    def step(self):
        super().step()
        #To complete
        

class SpeakingModel(Model):
    """ """
    def __init__(self):
        self.schedule = RandomActivation(self)
        self.__messages_service = MessageService(self.schedule)
        self.running = True

    def step(self):
        #To complete
        self.__messages_service.dispatch_messages()
        self.schedule.step()



if __name__ == "__main__":
    # Init the model and the agents
     #To complete
    speaking_model=SpeakingModel()

    MessageService.get_instance().set_instant_delivery(False)

    alice=SpeakingAgent(1,speaking_model,"Alice")

    bob=SpeakingAgent(2,speaking_model,"Bob")

    charles=BrookerAgent(3,speaking_model,"Charles")

    speaking_model.schedule.add(alice)
    speaking_model.schedule.add(bob)
    speaking_model.schedule.add(charles)

   
  

    # Launch the Communication part 

       # To complete
    
    message=Message(alice.get_name(),charles.get_name(),MessagePerformative.QUERY_REF,"Charles donnes moi la valeur de v")
    alice.send_message(message)

         
    
    
    
    #message=Message(bob.unique_id,charles.unique_id,MessagePerformative.QUERY_REF,"Charles donnes moi la valeur de v")
    
    #bob.send_message(message)

    step = 0
    while step < 10:
        speaking_model.step()
        step += 1
        print()
