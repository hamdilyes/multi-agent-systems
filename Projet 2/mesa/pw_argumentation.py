from mesa import Model
from mesa.time import RandomActivation
import json
import random
from communication.agent.CommunicatingAgent import CommunicatingAgent
from communication.mailbox.Mailbox import Mailbox
from communication.message.Message import Message
from communication.message.MessagePerformative import MessagePerformative
from communication.message.MessageService import MessageService
from communication.preferences.Preferences import Preferences
from communication.preferences.CriterionName import CriterionName
from communication.preferences.CriterionValue import CriterionValue
from communication.preferences.Value import Value
from communication.preferences.Item import Item
from communication.arguments.Argument import Argument
from communication.arguments.Comparison import Comparison
from communication.ArgumentAgent import ArgumentAgent


with open('data.json') as f:
    data = json.load(f)
    f.close()

List_items = [Item("Diesel Engine", "A super cool diesel engine"),
                Item("Electric Engine", "A very quiet engine")]

def transform_value(value):
    """ Transform the string value of the criterion into a correct value.
    """
    if value == 'VERY_BAD':
        return Value.VERY_BAD
    elif value == 'BAD':
        return Value.BAD
    elif value == 'GOOD':
        return Value.GOOD
    elif value == 'VERY_GOOD':
        return Value.VERY_GOOD
    
def transform_name(value):
    """ Transform the string value of the criterion into a correct value.
    """
    if value == 'PRODUCTION_COST':
        return CriterionName.PRODUCTION_COST
    elif value == 'ENVIRONMENT_IMPACT':
        return CriterionName.ENVIRONMENT_IMPACT
    elif value == 'CONSUMPTION':
        return CriterionName.CONSUMPTION
    elif value == 'DURABILITY':
        return CriterionName.DURABILITY
    elif value == 'NOISE':
        return CriterionName.NOISE
    


class ArgumentModel( Model ) :
    """ ArgumentModel which inherit from Model .
    """
    def __init__( self, N, max_steps ) :
        self.schedule = RandomActivation( self )
        self.__messages_service = MessageService( self.schedule )
        self.max_steps = max_steps
        for i in range(N):
            agent_pref = Preferences()
            a = ArgumentAgent(i, self, "Agent" + str(i), agent_pref , List_items)
            a.generate_preferences(List_items)
            a.List_Supporting_Proposal(List_items[0])
            a.List_Supporting_Proposal(List_items[1])
            self.schedule.add(a)

        self.running = True

    def step( self ) :
        self.__messages_service.dispatch_messages()
        self.schedule.step()



if __name__ == '__main__':
    ##### Init the model and the agents
    argument_model = ArgumentModel(N=2, max_steps=100)
    service = argument_model._ArgumentModel__messages_service # type: ignore

    ### Sender should be different from the receiver
    agents = random.sample(argument_model.schedule.agents, 2)
    
    sender = agents[0].get_name()
    receiver = agents[1].get_name()
    first_item = agents[0].preference.most_preferred(List_items)
    message = Message(sender, receiver, MessagePerformative.PROPOSE, first_item)
    agents[0].item_proposed.append(first_item)
    agents[0].proposed_item = first_item

    agents[0].send_message(message)
  
    ### steps
    while argument_model.running and argument_model.schedule.steps < argument_model.max_steps:
        argument_model.step()