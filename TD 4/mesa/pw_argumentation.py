#!/usr/bin/env python3
from mesa import Model
from mesa.time import RandomActivation
import pandas as pd
import json

from communication.agent.CommunicatingAgent import CommunicatingAgent
from communication.message.MessageService import MessageService
from communication.preferences.Preferences import Preferences
from communication.preferences.CriterionName import CriterionName
from communication.preferences.CriterionValue import CriterionValue
from communication.preferences.Value import Value
from communication.preferences.Item import Item


with open('data.json') as f:
    data = json.load(f)
    #close
    f.close()

def transform(value):
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

    def generate_preferences( self , List_items ):
        self.preference.set_criterion_name_list([CriterionName.PRODUCTION_COST])
        agent_data = data[str(self.unique_id)]

        for item in List_items:
            item_data = agent_data[item.get_name()]
            for criterion in self.preference.get_criterion_name_list():
                criterion_value = transform(item_data[criterion.name])

                self.preference.add_criterion_value(CriterionValue(item,criterion, criterion_value))
                                                  
                                                  #.add_criterion_value(CriterionValue(diesel_engine, CriterionName.DURABILITY,
                                                  #Value.VERY_GOOD))
                
        print(self.preference.get_criterion_value_list())

class ArgumentModel( Model ) :
    """ ArgumentModel which inherit from Model .
    """
    def __init__( self ) :
        self.schedule = RandomActivation( self )
        self.__messages_service = MessageService( self.schedule )
        for i in range(2):
            agent_pref = Preferences()
            a = ArgumentAgent(i, self, "Agent" + str(i), agent_pref )
            a.generate_preferences([Item("Diesel Engine", "A super cool diesel engine"), Item("Electric Engine", "A very quiet engine")])
            self.schedule.add(a)
            print(i)
           

        self.running = True

    def step( self ) :
        self.__messages_service.dispatch_messages()
        self.schedule.step()

    


if __name__ == '__main__':
    print('*---- Testing communication package ----')
    argument_model = ArgumentModel()
    print(argument_model)
    print(argument_model.schedule.agents)
  

    # To be completed