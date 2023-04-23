import json
import random

# List of sports
sports = ["Football", "Basketball", "Tennis", "Golf", "Swimming"]

# List of criteria
criteria = ["POPULARITY", "PHYSICAL_INTENSITY", "SKILL_REQUIRED", "TEAM_PLAY", "ENTERTAINMENT_VALUE"]

# Dictionary to store agent information
agents = {}

# Generate agents with random preference values
for agent_id in range(10):
    agent_prefs = {}
    # Generate random preference values for criteria

    # Generate random list of unique integer values from 1 to 5
    pref = random.sample(range(1, 6), 5)
    agent_prefs["Criteria_List"] = dict(zip(criteria, pref))
    # Generate preference values for sports
    for sport in sports:
        sport_prefs = {}
        # Generate random preference values for criteria
        for crit in criteria:
            # Generate random preference values from ["VERY_BAD", "BAD", "GOOD", "VERY_GOOD"]
            pref = random.choice(["VERY_BAD", "BAD", "GOOD", "VERY_GOOD"])
            sport_prefs[crit] = pref
        agent_prefs[sport] = sport_prefs
    agents[str(agent_id)] = agent_prefs

# Convert the dictionary to JSON
agents_json = json.dumps(agents, indent=4)

# save JSOn
with open('sport.json', 'w') as f:
    f.write(agents_json)
    f.close()
