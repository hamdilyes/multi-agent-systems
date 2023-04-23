from mesa import Model
from mesa.time import RandomActivation
import json
import random
from communication_sport.agent.CommunicatingAgent import CommunicatingAgent
from communication_sport.mailbox.Mailbox import Mailbox
from communication_sport.message.Message import Message
from communication_sport.message.MessagePerformative import MessagePerformative
from communication_sport.message.MessageService import MessageService
from communication_sport.preferences.Preferences import Preferences
from communication_sport.preferences.CriterionName import CriterionName
from communication_sport.preferences.CriterionValue import CriterionValue
from communication_sport.preferences.Value import Value
from communication_sport.preferences.Item import Item
from communication_sport.arguments.Argument import Argument
from communication_sport.arguments.Comparison import Comparison


with open('sport.json') as f:
    data = json.load(f)
    f.close()


def transform_value(value):
    """ Transform the string value of the criterion into a correct value.
    """
    return {
        'VERY_BAD': Value.VERY_BAD,
        'BAD': Value.BAD,
        'GOOD': Value.GOOD,
        'VERY_GOOD': Value.VERY_GOOD
    }.get(value)

def transform_name(value):
    """ Transform the string value of the criterion into a correct value.
    """
    return {
        'POPULARITY': CriterionName.POPULARITY,
        'PHYSICAL_INTENSITY': CriterionName.PHYSICAL_INTENSITY,
        'SKILL_REQUIRED': CriterionName.SKILL_REQUIRED,
        'TEAM_PLAY': CriterionName.TEAM_PLAY,
        'ENTERTAINMENT_VALUE': CriterionName.ENTERTAINMENT_VALUE
    }.get(value)

# Define sports as List_items
List_items = [
    Item("Basketball", "A popular team sport"),
    Item("Football", "A physical and intense team sport"),
    Item("Tennis", "An individual sport that requires skill"),
    Item("Swimming", "A sport with a focus on endurance"),
    Item("Golf", "A sport with an emphasis on entertainment value")
]
    
    
    

class ArgumentAgent( CommunicatingAgent ) :
    """ ArgumentAgent which inherit from CommunicatingAgent .
    """
    def __init__( self , unique_id , model , name , preferences, List_items ) :
        super().__init__( unique_id , model , name )
        self.model = model
        self.preference = preferences
        self.comparison = []
        self.item_proposed = []
        self.supporting_proposals = {}
        self.List_items = List_items
        self.proposed_item = None
        # Initialize the supporting_proposals dictionary with empty lists
        for item in self.List_items:
            self.supporting_proposals[item] = []
    
    def step( self ) :
        super().step()
        list_messages = self.get_new_messages()
        for message in list_messages:
            send = message.get_exp()
            dest = message.get_dest()
            #print(dest)
            dest_a = [i for i in self.model.schedule.agents if i.get_name() == dest][0]
            send_a = [i for i in self.model.schedule.agents if i.get_name() == send][0]
            item = message.get_content()
            # PROPOSE
            if message.get_performative() == MessagePerformative.PROPOSE:
                if dest_a.get_preference().is_item_among_top_10_percent(item, self.List_items):
                    self.send_message(Message(dest, send, MessagePerformative.ACCEPT, item))
                else:
                    self.send_message(Message(dest, send, MessagePerformative.ASK_WHY, item))
            # COMMIT
            elif message.get_performative() == MessagePerformative.COMMIT:
                self.model.running = False
                self.send_message(Message(dest, send, MessagePerformative.COMMIT, item))
                
            # ACCEPT
            elif message.get_performative() == MessagePerformative.ACCEPT:
                self.send_message(Message(dest, send, MessagePerformative.COMMIT, item))

            # ASK_WHY
            elif message.get_performative() == MessagePerformative.ASK_WHY:
                argument = Argument(boolean_decision=True, item=item)
                proposal = self.support_proposal(item)
                argument.add_premiss_couple_values(proposal.get_criterion_name(), proposal.get_value())
                self.send_message(Message(dest, send, MessagePerformative.ARGUE, argument))
                self.model.chosen_item = item

            # ARGUE
            elif message.get_performative() == MessagePerformative.ARGUE:
                argument = message.get_content()
                item = argument.item
                attack = self.attack_argument(send_a,argument)
                proposal = None
                if self.proposed_item is not None:
                    proposal = self.support_proposal(self.proposed_item)
                    #self.model.chosen_item = self.proposed_item

                # Decide to attack or not
                if attack[0]:
                    # Attack the argument
                    if isinstance(attack[1], Item):
                        self.send_message(Message(dest, send, MessagePerformative.PROPOSE,attack[1]))
                        self.proposed_item = attack[1]
                        self.item_proposed.append(attack[1])
                        self.model.chosen_item = attack[1]
                    else:
                        self.send_message(Message(dest, send, MessagePerformative.ARGUE,attack[1]))


                elif proposal is not None:
                    argument = Argument(boolean_decision=True, item=self.proposed_item)
                    argument.add_premiss_couple_values(proposal.get_criterion_name(), proposal.get_value())
                    self.send_message(Message(dest, send, MessagePerformative.ARGUE, argument))
                    self.model.chosen_item = self.proposed_item


                else :
                    #print(self.model.chosen_item)
                    self.send_message(Message(dest, send, MessagePerformative.ACCEPT, self.model.chosen_item))
                    
                

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
     
     
        
        for criterion in self.preference.get_criterion_value_list():
            if criterion.get_item() == item:
                criterion_value = self.preference.get_value(item, criterion.get_criterion_name())
                if criterion_value in [Value.GOOD, Value.VERY_GOOD]:
                    self.supporting_proposals[item].append(criterion)

        
        



    def support_proposal(self , item ) :
        """
        Used when the agent receives " ASK_WHY " after having proposed an item
        param item : str - name of the item which was proposed
        return : string - the strongest supportive argument
        """
        # To be completed
        if len(self.supporting_proposals[item]) == 0:
            return None
        proposal = self.supporting_proposals[item][0]
        self.supporting_proposals[item].remove(proposal)
        return proposal




    def attack_argument(self , sender, argument ) :
        """
        Write a method that decides whether an argument can be attacked or not. In our context the
        agent can attack or contradict an argument provided by another agent if:
        • The criterion is not important for him (regarding his order)
        • Its local value for the item is lower than the one of the other agent on the considered criteria
        • He prefers another item and he can defend it by an argument with a better value on the
        same criterion.
        """
        
        if argument.couple_values is not None:
            item = argument.item
            criterion = argument.couple_values.criterion_name
            value = argument.couple_values.value
            # The criterion is not important for him (regarding his order)
            if criterion in self.preference.get_criterion_name_list()[-1:-3:-1]:
                c_argument = Argument(True, self.proposed_item)
                proposal = None
                if self.proposed_item is not None:
                    proposal = self.support_proposal(self.proposed_item)
                if proposal is not None:
                    comparison = (proposal.get_criterion_name(), argument.couple_values.criterion_name)
                    if comparison not in self.comparison:
                        self.comparison.append(comparison)
                        c_argument.add_premiss_couple_values(proposal.get_criterion_name(), proposal.get_value())
                        c_argument.add_premiss_comparison(proposal.get_criterion_name(),argument.couple_values.criterion_name)
                        #print("1")
                        self.model.chosen_item = self.proposed_item
                        return True, c_argument
     

            # Its local value for the item is lower than the one of the other agent on the considered criteria
            b = False
            cr = None
            for crit in self.preference.get_criterion_value_list():
                if crit.get_item() == item and crit.get_criterion_name() == criterion and crit.get_value() in [Value.BAD, Value.VERY_BAD]:
                    b = True
                    cr = crit
                    break
            if b and value in [Value.GOOD, Value.VERY_GOOD]:
                c_argument = Argument(False, item)
                c_argument.add_premiss_couple_values(cr.get_criterion_name(), cr.get_value())
                self.chosen_item = self.proposed_item
                #print("2")
                return True, c_argument


        # The criterion is not important for him (regarding his order)        
        if argument.comparison is not None:
            b_criterion = argument.comparison.best_criterion_name
            w_criteria = argument.comparison.worst_criterion_name
            for crit in self.preference.get_criterion_name_list()[:2]:
                if crit != b_criterion and (crit, b_criterion) not in self.comparison:
                    self.comparison.append((crit, b_criterion))
                    current_item = sender.proposed_item
                    if current_item is not None:
                        c_argument = Argument(False, current_item)
                        c_argument.add_premiss_comparison(crit, b_criterion)
                        c_argument.add_premiss_couple_values(crit, self.preference.get_value(current_item, crit))
                        self.model.chosen_item = self.proposed_item
                    #print("3")
                        return True, c_argument
                



        # He prefers another item and he can defend it by an argument with a better value on the same criterion.
        if argument.couple_values is not None:
            criterion = argument.couple_values.criterion_name
            preferred_item = self.preference.most_preferred(self.List_items)
            if preferred_item not in self.item_proposed and criterion is not None and preferred_item != argument.item :
                self.item_proposed.append(preferred_item)
                #print("4")
                self.model.chosen_item = preferred_item
                return True, preferred_item

        
        next_items = [item for item in self.List_items if item not in self.item_proposed + sender.item_proposed]
        if len(next_items) > 0:
            next_item = next_items[0]
            for item in next_items[1:]:
                if self.preference.is_preferred_item(item, next_item):
                    next_item = item
            self.item_proposed.append(next_item)
            return True, next_item
                
            
        
        self.model.chosen_item = sender.proposed_item
        #print(sender,sender.proposed_item)

        return False, 0