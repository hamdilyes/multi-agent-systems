from mesa import Model
from mesa.time import RandomActivation

from communication.agent.CommunicatingAgent import CommunicatingAgent
from communication.message.MessageService import MessageService
from communication.preferences.Preferences import Preferences
from communication.preferences.CriterionName import CriterionName
from communication.preferences.CriterionValue import CriterionValue
from communication.preferences.Value import Value
from communication.preferences.Item import Item


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
        self.preference.set_criterion_name_list([CriterionName.PRODUCTION_COST, CriterionName.ENVIRONMENT_IMPACT,
                                        CriterionName.CONSUMPTION, CriterionName.DURABILITY,
                                        CriterionName.NOISE])

        for item in List_items:
            self.preference.add_criterion_value(CriterionValue(item, CriterionName.PRODUCTION_COST,
                                                        Value.VERY_GOOD))
            self.preference.add_criterion_value(CriterionValue(item, CriterionName.CONSUMPTION,
                                                        Value.GOOD))
            self.preference.add_criterion_value(CriterionValue(item, CriterionName.DURABILITY,
                                                        Value.VERY_GOOD))
            self.preference.add_criterion_value(CriterionValue(item, CriterionName.ENVIRONMENT_IMPACT,
                                                        Value.VERY_BAD))
            self.preference.add_criterion_value(CriterionValue(item, CriterionName.NOISE,
                                                        Value.VERY_BAD))

class ArgumentModel( Model ) :
    """ ArgumentModel which inherit from Model .
    """
    def __init__( self ) :
        self.schedule = RandomActivation( self )
        self.__messages_service = MessageService( self.schedule )
        for i in range(2):
            agent_pref = Preferences()
            a = ArgumentAgent(i, self, "Agent" + str(i), agent_pref )
            self.schedule.add(a)
            a.generate_preferences()
            self.schedule.add(a)

        self.running = True

    def step( self ) :
        self.__messages_service.dispatch_messages()
        self.schedule.step()


if __name__ == " __main__ ":
    argument_model = ArgumentModel()

    # To be completed