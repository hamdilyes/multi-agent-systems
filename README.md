# Multi-agent systems
## Projet 1 : [Preys & Predators](https://docs.google.com/document/d/118d3Ynb-69fR4n2nVzAx7hxlzpl_CJVOSKRZr7UUY0U/edit?usp=sharing)

## Projet 2 : Argumentation-based dialogue for choosing a sport
### Overview
The goal is to simulate an argumentation-based dialogue between artificial agents which will interact to make a joint decision regarding choosing the best sport. One can then imagine several applications. For instance by studying the most impactful arguments.

### Agent Preferences
#### Data about sports
We prepare a data.json file beforehand. An object in this file represents an agent (the implementation is meant for 2 so far). It is represented by an integer and comes with a "Criteria_List" property which gives the ordered criteria importance for the agent. Then there is a property for each of the sports to compare. Each property contains a list of key-value pairs to capture the agent's rating of the sport for each criteria. The file Value.py defines the possible ratings and CriteriaName.py defines the criteria list we chose:
* a
* b
* c
#### Get preferences
How an agent sets and compares their preferences regarding different sports and criteria is defined in the Preference class which will be an attribute of an agent object. The method generate_preferences of the ArgumentAgent class enables to generate the preferences object by reading the data file. There are 2 auxiliary functions transform_name and transform_value to switch from strings in the json file to correct criteria names and values.

### Communication
We use 5 message performatives: PROPOSE - ASK_WHY - ARGUE - ACCEPT - COMMIT.

### Arguments


### Selecting arguments
The method List_Supporting_Proposal, takes a sport as a parameter and generates a list of premises that can be used to support the sport. It iterates through the preference criteria of the agent and checks if the criterion is related to the given sport. If the criterion's value is GOOD or VERY_GOOD. The method returns the supporting_proposals list sorted by order of importance based on the agent's preferences.

The method List_Attacking_Proposal, does the same but this time to attack a sport.

The method support_proposal, is used when the agent receives an ASK_WHY message after having proposed a sport. It takes the sport as a parameter and returns the strongest supportive argument for it by calling the List_Supporting_Proposal method and returning the first element of the resulting list.

### Relations among arguments


### Simulation
#### How a discussion goes
Randomly choose agent A to go first. A starts by a PROPOSE performative to propose its best sport. Another agent, B, will enter in dialogue with it and reply with an ACCEPT if the sport is also its best one, otherwise it will reply with an ASK_WHY. A replies with an ARGUE which means

#### Launch
Run the pw_argumentation.py file, sit back and watch the agents discuss!

## Results
### Statistics about our simulations


## Next steps
Now that our 2-agent argumentation-based dialogue system is fully functional, we need to make it multi-agent where interaction is still run between each pair of agents. This involves implementing new strategies for managing the dialogue flow as well as deciding when the common agreement is reached.
