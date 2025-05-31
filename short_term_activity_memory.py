import csv

# Dictionary to track short-term activity for each agent
activity_memory = {}

def initialize_activity_memory(agent_list):
    """
    Initializes the activity memory for each agent in the list.
    Each agent gets a list of four integers corresponding to:
    [posting, inactivity, sharing, interacting]
    """
    for agent in agent_list:
        activity_memory[agent.name.lower()] = [0, 0, 0, 0]

def update_activity(agent_name: str, choice: int):
    """
    Updates the activity counters for the specified agent.

    Parameters:
    - agent_name (str): Name of the agent
    - choice (int): Action choice
      (1 = publish, 2 = inactivity, 3 = share, 4-6 = interaction)

    Behavior:
    - Resets the counter of the performed activity to 0
    - Increments the counters of all other activities by 1
    """
    agent_id = agent_name.lower()
    if agent_id not in activity_memory:
        # PER ORA USO RAISE PER BLOCCARE LA SIM IN CASO DI ERRORE, POI NEL CASO LA GESTISCO
        raise ValueError(f"Agent {agent_name} not initialized in activity memory.")

    if choice in [1, 2, 3]:
        activity_index = choice - 1
    elif choice in [4, 5, 6]:
        activity_index = 3
    else:
        # PER ORA USO RAISE PER BLOCCARE LA SIM IN CASO DI ERRORE, POI NEL CASO LA GESTISCO
        raise ValueError(f"Invalid choice {choice}. Must be in range 1–6.")

    for i in range(4):
        if i == activity_index:
            activity_memory[agent_id][i] = 0
        else:
            activity_memory[agent_id][i] += 1

def get_activity(agent_name: str):
    """
    Returns the activity list for the specified agent.
    """
    return activity_memory.get(agent_name.lower(), None)

# def reset_all_activities():
#     """
#     Resets all activity counters for all agents to zero.
#     """
#     for agent_id in activity_memory:
#         activity_memory[agent_id] = [0, 0, 0, 0]

def save_activity_memory_to_csv(filepath="Output/activity_memory.csv"):
    with open(filepath, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Agent", "Posting", "Inactivity", "Sharing", "Interacting"])
        for agent, counters in activity_memory.items():
            writer.writerow([agent] + counters)


def load_activity_memory_from_csv(filepath="Output/activity_memory.csv"):
    activity_memory.clear()
    with open(filepath, mode="r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            agent = row["Agent"].lower()
            counters = [int(row["Posting"]), int(row["Inactivity"]), int(row["Sharing"]), int(row["Interacting"])]
            activity_memory[agent] = counters