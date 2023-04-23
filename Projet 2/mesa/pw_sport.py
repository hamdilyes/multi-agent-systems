from mesa import Model
from mesa.time import RandomActivation
import matplotlib.pyplot as plt
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
from communication_sport.ArgumentAgent import ArgumentAgent

message_service = MessageService(RandomActivation(Model))


with open('sport.json') as f:
    data = json.load(f)

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


class ArgumentModel( Model ) :
    """ ArgumentModel which inherit from Model .
    """
    def __init__( self, N, max_steps ) :
        self.schedule = RandomActivation( self )
        self.__messages_service = message_service
        self.__messages_service.update(self.schedule)
        self.max_steps = max_steps
        self.chosen_item = None
        ind1,ind2 = random.sample(range(0,9),2)
        for i in range(N):
            agent_pref = Preferences()
            if i %2 == 0:
                a = ArgumentAgent(ind1, self, "Agent" + str(ind1), agent_pref , List_items)
            else:
                a = ArgumentAgent(ind2, self, "Agent" + str(ind2), agent_pref , List_items)
            a.generate_preferences(List_items)
            for item in List_items:
                a.List_Supporting_Proposal(item)
            self.schedule.add(a)

        self.running = True

    def step( self ) :
        self.__messages_service.dispatch_messages()
        self.schedule.step()



if __name__ == '__main__':
    ##### Init the model and the agents
    # run the model 100 times and save the chose sport
    chosen_sport = []
    for i in range(100):
        argument_model = ArgumentModel(N=2, max_steps=100)
        service = argument_model._ArgumentModel__messages_service # type: ignore

        ### Sender should be different from the receiver
        agents = random.sample(argument_model.schedule.agents, 2)
        
        sender = agents[0].get_name()
        receiver = agents[1].get_name()
        first_item = random.choice(List_items)
        message = Message(sender, receiver, MessagePerformative.PROPOSE, first_item)
        agents[0].item_proposed.append(first_item)
        agents[0].proposed_item = first_item
        argument_model.chosen_item = first_item
        agents[0].send_message(message)

        ### steps
        while argument_model.running and argument_model.schedule.steps < argument_model.max_steps:
            argument_model.step()

        chosen_sport.append(argument_model.chosen_item.get_name())
    plt.hist(chosen_sport)
    #plt.show()
    plt.savefig('histogram.png')