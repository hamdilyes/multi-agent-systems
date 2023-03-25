#!/usr/bin/env python3
from mesa import Model
from mesa.time import RandomActivation
import json

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



with open('data.json') as f:
    data = json.load(f)
    f.close()

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
    


class ArgumentAgent( CommunicatingAgent ) :
    """ ArgumentAgent which inherit from CommunicatingAgent .
    """
    def __init__( self , unique_id , model , name , preferences ) :
        super().__init__( unique_id , model , name )
        self.preference = preferences

    def step( self ) :
        super().step()

    def get_preference( self ):
        return self.preference
    
    # [CriterionName.PRODUCTION_COST, CriterionName.ENVIRONMENT_IMPACT,
    #  CriterionName.CONSUMPTION, CriterionName.DURABILITY,
    #  CriterionName.NOISE]
    def generate_preferences( self , List_items ):
        agent_data = data[str(self.unique_id)]

        # get the list of criteria, non-ordered
        criteria_list = agent_data["Criteria_List"].keys()
        # sort criteria_list according to the values of the dictionary
        criteria_list = sorted(criteria_list, key=lambda x: agent_data["Criteria_List"][x])
        # transform the criteria_list into a list of CriterionName
        criteria_list = [transform_name(x) for x in criteria_list]
        self.preference.set_criterion_name_list(criteria_list)

        for item in List_items:
            item_data = agent_data[item.get_name()]
            for criterion in self.preference.get_criterion_name_list():
                criterion_value = transform_value(item_data[criterion.name])

                self.preference.add_criterion_value(CriterionValue(item, criterion, criterion_value))
                
        # print(self.preference.get_criterion_value_list())

class ArgumentModel( Model ) :
    """ ArgumentModel which inherit from Model .
    """
    def __init__( self, N, max_steps ) :
        self.schedule = RandomActivation( self )
        self.__messages_service = MessageService( self.schedule )
        self.max_steps = max_steps
        for i in range(N):
            agent_pref = Preferences()
            a = ArgumentAgent(i, self, "Agent" + str(i), agent_pref )
            List_items = [Item("Diesel Engine", "A super cool diesel engine"),
                          Item("Electric Engine", "A very quiet engine")]
            a.generate_preferences(List_items)
            self.schedule.add(a)           

        self.running = True

    def step( self ) :
        self.__messages_service.dispatch_messages()
        self.schedule.step()



if __name__ == '__main__':
    # Init the model and the agents
    argument_model = ArgumentModel(N=2, max_steps=100)
    service = argument_model._ArgumentModel__messages_service
    
    # Launch the Communication part
    # define the messages
    message_list = [
        Message("Agent0", "Agent1", MessagePerformative.PROPOSE, Item("Diesel Engine", "A super cool diesel engine")),
        Message("Agent1", "Agent0", MessagePerformative.ACCEPT, Item("Diesel Engine", "A super cool diesel engine"))
        ]

    # send the messages
    for i in range(len(message_list)):
        service.send_message(message_list[i])
        print(message_list[i].__str__())

    # steps
    while argument_model.running and argument_model.schedule.steps < argument_model.max_steps:
        argument_model.step()