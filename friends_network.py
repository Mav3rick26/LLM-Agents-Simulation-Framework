import numpy as np
import pandas as pd
from short_term_memory import short_term_memory
from short_term_memory import embedding_function
from long_term_memory import long_term_memory
from sklearn.metrics.pairwise import cosine_similarity
from utils import read_from_file, get_embedding
import math

friends_network = {}  # Dictionary of friends


def init_friends_network(agent_list):
    for agent in agent_list:
        friends_network[agent] = []


def get_friends_network():
    for agent, friends in friends_network.items():
        print(f"Agent name: {agent.name}")
        print("Following: ", ', '.join(friend.name for friend in friends) if friends else "No friends.")
        print("\n")


def get_follow_list(agent):
    return friends_network.get(agent, [])


def get_follower_list(agent):
    return [other_agent for other_agent, friends in friends_network.items() if agent in friends]


def add_follow(agent, friend):
    if agent not in friends_network:  # Aggiungere l'agente al dizionario se non esiste
        friends_network[agent] = []

    if agent != friend:
        if friend not in friends_network[agent]:  # Aggiungere il friend solo se non è già presente
            friends_network[agent].append(friend)
            return True
    else:
        return False


# def get_content_similarity(first_agent, second_agent):
#     try:
#         first_agent_stm_res = short_term_memory.get(
#             where={
#                 "Author": {
#                     "$eq": str(first_agent.name.lower())
#                 }
#             },
#             include=["documents", "embeddings"]
#         )

#         first_agent_ltm_res = long_term_memory.get(
#             where={
#                 "Author": {
#                     "$eq": str(first_agent.name.lower())
#                 }
#             },
#             include=["documents", "embeddings"]
#         )

#         second_agent_stm_res = short_term_memory.get(
#             where={
#                 "Author": {
#                     "$eq": str(second_agent.name.lower())
#                 }
#             },
#             include=["documents", "embeddings"]
#         )

#         second_agent_ltm_res = long_term_memory.get(
#             where={
#                 "Author": {
#                     "$eq": str(second_agent.name.lower())
#                 }
#             },
#             include=["documents", "embeddings"]
#         )

#         first_agent_stm_embeddings = first_agent_stm_res["embeddings"]
#         first_agent_ltm_embeddings = first_agent_ltm_res["embeddings"]
#         second_agent_stm_embeddings = second_agent_stm_res["embeddings"]
#         second_agent_ltm_embeddings = second_agent_ltm_res["embeddings"]

#         # Combina le embedding STM e LTM per ciascun agente
#         first_agent_embeddings = first_agent_stm_embeddings + first_agent_ltm_embeddings
#         second_agent_embeddings = second_agent_stm_embeddings + second_agent_ltm_embeddings

#         # Calcola la similarità coseno tra ciascuna coppia di embedding
#         similarities = []
#         for first_agent_embedding in first_agent_embeddings:
#             for second_agent_embedding in second_agent_embeddings:
#                 similarity = cosine_similarity([first_agent_embedding], [second_agent_embedding])[0][0]
#                 similarities.append(similarity)

#         # Calcola la media delle similarità
#         average_similarity = np.mean(similarities) if similarities else float('NaN')

#         # Restituisce la media della similarità
#         return average_similarity
#     except Exception as e:
#         print("Cannot get content similarity: ", e)
#         return float('NaN')


# def get_suggested_follow_list(agent, agent_list, agent_friends_list):
#     similarities = []
#     for potential_follow in agent_list:
#         if potential_follow != agent:
#             if potential_follow.name not in [a.name for a in agent_friends_list]:
#                 content_similarity = get_content_similarity(agent, potential_follow)
#                 if content_similarity != 'nan':
#                     similarities.append({
#                         'agent': potential_follow,
#                         'similarity': content_similarity
#                     })

#     # Ordina la lista delle similarità in ordine decrescente
#     similarities.sort(key=lambda x: x['similarity'], reverse=True)
#     return similarities


def load_friends_network(csv_file_path, agent_list):
    # print(f'Lunghezza lista: {len(agent_list)}')
    selected_agent = None
    selected_followed_agent = None
    df = pd.read_csv(csv_file_path)
    for index, row in df.iterrows():
        agent_name = row['Agent']
        # print('Agent name: ', agent_name)
        for agent in agent_list:
            if agent.name == agent_name:
                selected_agent = agent
                # print('Selected agent: ', selected_agent.name)
        followed_agent_name = row['Followed Agent']
        # print('Followed agent name: ', followed_agent_name)
        for agent in agent_list:
            if agent.name == followed_agent_name:
                selected_followed_agent = agent
                # print('Selected followed agent: ', selected_followed_agent.name)
        is_agent_followed = add_follow(selected_agent, selected_followed_agent)
        # print('Is agent followed: ', is_agent_followed)
        # print('--------------------------------')
        if not is_agent_followed:
            print("Error loading friends network.")



    

# def get_embedding(text):
#     return embedding_function([text])[0]



def agent_has_published(agent):
    stm = short_term_memory.get(where={"Author": {"$eq": agent.name.lower()}}, include=["documents"])
    ltm = long_term_memory.get(where={"Author": {"$eq": agent.name.lower()}}, include=["documents"])
    return len(stm["documents"]) > 0 or len(ltm["documents"]) > 0



def get_embedding_source(agent, personality_folder):
    if agent_has_published(agent):
        stm = short_term_memory.get(where={"Author": {"$eq": agent.name.lower()}}, include=["embeddings"])
        ltm = long_term_memory.get(where={"Author": {"$eq": agent.name.lower()}}, include=["embeddings"])
        return stm["embeddings"] + ltm["embeddings"]
    else:
        personality_text = read_from_file(f"{agent.name.lower()}.txt", personality_folder)
        return [get_embedding(personality_text)]
    

    
def get_content_similarity(first_agent, second_agent, personality_folder):
    try:
        first_embeddings = get_embedding_source(first_agent, personality_folder)

        # Second agent: solo STM+LTM (mai la personalità)
        stm = short_term_memory.get(where={"Author": {"$eq": second_agent.name.lower()}}, include=["embeddings"])
        ltm = long_term_memory.get(where={"Author": {"$eq": second_agent.name.lower()}}, include=["embeddings"])
        second_embeddings = stm["embeddings"] + ltm["embeddings"]

        if not first_embeddings or not second_embeddings:
            return float('NaN')

        similarities = [
            cosine_similarity([e1], [e2])[0][0]
            for e1 in first_embeddings
            for e2 in second_embeddings
        ]

        return np.mean(similarities) if similarities else float('NaN')

    except Exception as e:
        print("Cannot get content similarity:", e)
        return float('NaN')
    

# def get_suggested_follow_list(agent, agent_list, agent_friends_list, personality_folder):
#     similarities = []
#     for potential_follow in agent_list:
#         if potential_follow != agent and potential_follow.name not in [a.name for a in agent_friends_list]:
#             content_similarity = get_content_similarity(agent, potential_follow, personality_folder)
#             #if content_similarity != 'nan':  #errore perché non è un float?
#                 similarities.append({
#                     'agent': potential_follow,
#                     'similarity': content_similarity
#                 })
#     similarities.sort(key=lambda x: x['similarity'], reverse=True)
#     return similarities


def get_suggested_follow_list(agent, agent_list, agent_friends_list, personality_folder):
    similarities = []
    for potential_follow in agent_list:
        if potential_follow != agent and potential_follow.name not in [a.name for a in agent_friends_list]:
            content_similarity = get_content_similarity(agent, potential_follow, personality_folder)
    
            if not math.isnan(content_similarity):
                similarities.append({
                    'agent': potential_follow,
                    'similarity': content_similarity
                })

    similarities.sort(key=lambda x: x['similarity'], reverse=True)
    return similarities