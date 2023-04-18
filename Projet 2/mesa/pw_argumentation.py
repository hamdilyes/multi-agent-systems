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
    

class ArgumentAgent( CommunicatingAgent ) :
    """ ArgumentAgent which inherit from CommunicatingAgent .
    """
    def __init__( self , unique_id , model , name , preferences ) :
        super().__init__( unique_id , model , name )
        self.preference = preferences

    def step( self ) :
        super().step()
        list_messages = self.get_new_messages()
        for message in list_messages:
            send = message.get_exp()
            dest = message.get_dest()
            dest_a = service.find_agent_from_name(dest)
            item = message.get_content()
            # PROPOSE
            if message.get_performative() == MessagePerformative.PROPOSE:
                if dest_a.get_preference().is_item_among_top_10_percent(item, List_items):
                    self.send_message(Message(dest, send, MessagePerformative.ACCEPT, item))
                else:
                    self.send_message(Message(dest, send, MessagePerformative.ASK_WHY, item))
            # COMMIT
            elif message.get_performative() == MessagePerformative.COMMIT:
                self.send_message(Message(dest, send, MessagePerformative.COMMIT, item))
                self.model.running = False
            # ACCEPT
            elif message.get_performative() == MessagePerformative.ACCEPT:
                self.send_message(Message(dest, send, MessagePerformative.COMMIT, item))
            # ASK_WHY
            elif message.get_performative() == MessagePerformative.ASK_WHY:
                argument = Argument(boolean_decision=True, item=item)
                proposal = self.support_proposal(item)
                argument.add_premiss_couple_values(proposal.get_criterion_name(), proposal.get_value())
                self.send_message(Message(dest, send, MessagePerformative.ARGUE, argument))
            # ARGUE
            elif message.get_performative() == MessagePerformative.ARGUE:
                #print("Hey")
                argument = message.get_content()
                #print(argument)
                item = argument.item
                attack = self.attack_argument(argument)
                #print(attack)
                if not attack[0]:
                    #print("I accept")
                    self.send_message(Message(dest, send, MessagePerformative.ACCEPT, item))
                else:
                    #print("I counter-argue")
                    counter_argument = Argument(boolean_decision=False, item=item)
                    if attack[1] in (1,2):
                        crit = [c for c in self.preference.get_criterion_value_list() if c.get_item() == item][0]
                        counter_argument.add_premiss_comparison(crit.get_criterion_name(),argument.couple_values.criterion_name)
                        counter_argument.add_premiss_couple_values(crit.get_criterion_name(),crit.get_value() )
                        self.send_message(Message(dest, send, MessagePerformative.ARGUE,counter_argument ))
                    elif attack[1] == 3:
                        self.send_message(Message(dest, send, MessagePerformative.PROPOSE, self.preference.most_preferred(List_items)))


    def get_preference( self ):
        return self.preference
    
    
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
    

    def List_Supporting_Proposal(self, item):
        """ Generate a list of premisses which can be used to support an item
        param item : Item - name of the item
        return : list of all premisses PRO an item ( sorted by order of importance
        based on agents preferences )
        """
        # To be completed
        supporting_proposals = []
        for criterion in self.preference.get_criterion_value_list():
            if criterion.get_item() == item:
                criterion_value = self.preference.get_value(item, criterion.get_criterion_name())
                if criterion_value in [Value.GOOD, Value.VERY_GOOD]:
                    supporting_proposals.append(criterion)
        
        return supporting_proposals
    

    def List_Attacking_Proposal(self, item):
        """ Generate a list of premisses which can be used to attack an item
        param item : Item - name of the item
        return : list of all premisses CON an item ( sorted by order of importance
        based on agents preferences )
        """
        # To be completed
        attacking_proposals = []

        for criterion in self.preference.get_criterion_value_list():
            if criterion.get_item() == item:
                criterion_value = self.preference.get_value(item, criterion.get_criterion_name())
                if criterion_value in [Value.BAD, Value.VERY_BAD]:
                    attacking_proposals.append(criterion)

        return attacking_proposals


    def support_proposal(self , item ) :
        """
        Used when the agent receives " ASK_WHY " after having proposed an item
        param item : str - name of the item which was proposed
        return : string - the strongest supportive argument
        """
        # To be completed
        return self.List_Supporting_Proposal(item)[0]


    def parse_argument(self, argument):
        """ Parse an argument and return the list of premisses
        param argument : Argument
        return : list of CriterionValue
        """
        # To be completed
        return [argument.comparison , argument.couple_values]


    def attack_argument(self , argument ) :
        """
        Write a method that decides whether an argument can be attacked or not. In our context the
        agent can attack or contradict an argument provided by another agent if:
        • The criterion is not important for him (regarding his order)
        • Its local value for the item is lower than the one of the other agent on the considered criteria
        • He prefers another item and he can defend it by an argument with a better value on the
        same criterion.
        """
        # The criterion is not important for him (regarding his order)
        if argument.couple_values is not None:
            criterion = argument.couple_values.criterion_name
            value = argument.couple_values.value
            if criterion in self.preference.get_criterion_name_list()[-1:-2:-1]:
                return True, 1

            # Its local value for the item is lower than the one of the other agent on the considered criteria
            b = False
            for crit in self.preference.get_criterion_value_list():
                if crit.get_criterion_name() == criterion and crit.get_value() in [Value.BAD, Value.VERY_BAD]:
                    b = True
                    cr = crit
                    break
            if b and value in [Value.GOOD, Value.VERY_GOOD]:
                return True, 2

        # He prefers another item and he can defend it by an argument with a better value on the same criterion.
        if self.preference.most_preferred(List_items) != argument.item:
            return True, 3

        return False, 0
    

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
            a.generate_preferences(List_items)
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
    message = Message(sender, receiver, MessagePerformative.PROPOSE, List_items[0])

    agents[0].send_message(message)
  
    ### steps
    while argument_model.running and argument_model.schedule.steps < argument_model.max_steps:
        argument_model.step()