import json
import os
import re
import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')  # Embedding model

llama3 = {
    "config_list": [
        {
            "model": "meta-llama-3.1-8b-instruct",
            "base_url": "http://localhost:1234/v1",
            "api_key": "lm-studio",
        },
    ],
    "cache_seed": None,  # Disable caching.
}


# GENERAL FUNCTIONS
def save_personality_to_file(content, filename, folder):
    if not filename.endswith(".txt"):
        filename += ".txt"

    # Verifica se la cartella esiste, altrimenti la crea
    if not os.path.exists(folder):
        os.makedirs(folder)

    # Componi il percorso completo del file
    file_path = os.path.join(folder, filename)

    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content)


def read_from_file(filename, folder):
    # Componi il percorso completo del file
    file_path = os.path.join(folder, filename)

    if not os.path.exists(file_path):
        return "File not found."  # Il file non esiste

    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    return content


def from_string_to_json(text):
    try:
        # Prova a caricare la stringa JSON utilizzando il modulo json
        json_data = json.loads(text)
        return json_data
    except json.JSONDecodeError:
        # Se il parsing JSON fallisce, prova a estrarre il primo blocco JSON
        match = re.search(r'{(.*?)}', text, re.DOTALL)
        if match:
            json_text = match.group(1)
            json_text = json_text.strip()
            try:
                # Tentativo di caricare il testo JSON estratto e formattarlo con i doppi apici
                json_data = json.loads("{" + json_text + "}")
                return json_data
            except json.JSONDecodeError as e:
                print(f"JSON string parsing error: {e}")

    # Se tutto fallisce, restituisci un dizionario vuoto
    return {}


def get_unique_contents(related_content):
    seen = {}
    unique_contents = []
    for doc in related_content['documents'][0]:
        if doc not in seen:
            seen[doc] = True
            unique_contents.append(doc)
    return unique_contents


def related_contents_to_string(content_list):
    related_content_string = ""
    for content in content_list[:10]:
        related_content_string += "\"" + content + "\"\n"
    return related_content_string


def get_agent_from_agent_list(agent_list, agent_name):
    for agent in agent_list:
        if agent.name.lower() == agent_name:
            return agent
    return 'ERROR: Agent not found.'


def suggested_follows_to_string(suggestion_list, personality_folder):
    suggested_follows_string = ""
    for follow_suggestion in suggestion_list[:5]:
        suggested_agent = follow_suggestion['agent']
        suggested_agent_personality = read_from_file(f"{suggested_agent.name.lower()}.txt", personality_folder)
        suggested_follows_string += "\"" + str(follow_suggestion['agent'].name) + "\" - Personality: " + suggested_agent_personality + "\n"
    return suggested_follows_string


# FUNCTIONS FOR CHECKING THE FORMAT OF USER RESPONSES
def check_choice_reason_format(user_proxy, agent):
    answer_correct_format = False
    attempt = 0
    while not answer_correct_format:
        answer = user_proxy.last_message(agent)["content"]
        json_answer = from_string_to_json(answer)

        if all(key.lower() in map(str.lower, json_answer) for key in ["Choice", "Reason"]) and len(json_answer) == 2 and all(isinstance(value, str) for value in json_answer.values()):
            answer_correct_format = True
        else:
            attempt += 1
            if attempt <= 3:
                user_proxy.initiate_chat(
                    agent,
                    message=read_from_file("check_choice_reason_format", "Prompt/errors"),
                    clear_history=False
                )
            else:
                answer_correct_format = True
                json_answer = {
                    "Choice": "2",
                    "Reason": "Auto",
                    "New content": "N/A"
                }
    return json_answer


def check_new_content_format(user_proxy, agent):
    answer_correct_format = False
    attempt = 0
    while not answer_correct_format:
        answer = user_proxy.last_message(agent)["content"]
        json_answer = from_string_to_json(answer)

        if all(key.lower() in map(str.lower, json_answer) for key in ["New content"]) and len(json_answer) == 1 and all(isinstance(value, str) for value in json_answer.values()):
            answer_correct_format = True
        else:
            attempt += 1
            if attempt <= 3:
                user_proxy.initiate_chat(
                    agent,
                    message=read_from_file("check_new_content_format", "Prompt/errors"),
                    clear_history=False
                )
            else:
                answer_correct_format = True
                json_answer = {
                    "Choice": "2",
                    "Reason": "Auto",
                    "New content": "N/A"
                }
    return json_answer


def check_shared_content_format(user_proxy, agent):
    answer_correct_format = False
    attempt = 0
    while not answer_correct_format:
        answer = user_proxy.last_message(agent)["content"]
        json_answer = from_string_to_json(answer)

        if all(key.lower() in map(str.lower, json_answer) for key in ["Shared content"]) and len(json_answer) == 1 and all(isinstance(value, str) for value in json_answer.values()):
            answer_correct_format = True
        else:
            attempt += 1
            if attempt <= 3:
                user_proxy.initiate_chat(
                    agent,
                    message=read_from_file("check_shared_content_format", "Prompt/errors"),
                    clear_history=False
                )
            else:
                answer_correct_format = True
                json_answer = {
                    "Choice": "2",
                    "Reason": "Auto",
                    "New content": "N/A"
                }
    return json_answer


def check_liked_content_format(user_proxy, agent):
    answer_correct_format = False
    attempt = 0
    while not answer_correct_format:
        answer = user_proxy.last_message(agent)["content"]
        json_answer = from_string_to_json(answer)

        if all(key.lower() in map(str.lower, json_answer) for key in ["Liked content"]) and len(json_answer) == 1 and all(isinstance(value, str) for value in json_answer.values()):
            answer_correct_format = True
        else:
            attempt += 1
            if attempt <= 3:
                user_proxy.initiate_chat(
                    agent,
                    message=read_from_file("check_liked_content_format", "Prompt/errors"),
                    clear_history=False
                )
            else:
                answer_correct_format = True
                json_answer = {
                    "Choice": "2",
                    "Reason": "Auto",
                    "New content": "N/A"
                }
    return json_answer


def check_disliked_content_format(user_proxy, agent):
    answer_correct_format = False
    attempt = 0
    while not answer_correct_format:
        answer = user_proxy.last_message(agent)["content"]
        json_answer = from_string_to_json(answer)

        if all(key.lower() in map(str.lower, json_answer) for key in ["Disliked content"]) and len(json_answer) == 1 and all(isinstance(value, str) for value in json_answer.values()):
            answer_correct_format = True
        else:
            attempt += 1
            if attempt <= 3:
                user_proxy.initiate_chat(
                    agent,
                    message=read_from_file("check_disliked_content_format", "Prompt/errors"),
                    clear_history=False
                )
            else:
                answer_correct_format = True
                json_answer = {
                    "Choice": "2",
                    "Reason": "Auto",
                    "New content": "N/A"
                }
    return json_answer


def check_commented_content_format(user_proxy, agent):
    answer_correct_format = False
    attempt = 0
    while not answer_correct_format:
        answer = user_proxy.last_message(agent)["content"]
        json_answer = from_string_to_json(answer)

        if all(key.lower() in map(str.lower, json_answer) for key in ["Commented content"]) and len(json_answer) == 1 and all(isinstance(value, str) for value in json_answer.values()):
            answer_correct_format = True
        else:
            attempt += 1
            if attempt <= 3:
                user_proxy.initiate_chat(
                    agent,
                    message=read_from_file("check_commented_content_format", "Prompt/errors"),
                    clear_history=False
                )
            else:
                answer_correct_format = True
                json_answer = {
                    "Choice": "2",
                    "Reason": "Auto",
                    "New content": "N/A"
                }
    return json_answer


def check_conversation_1_to_1_format(user_proxy, agent):
    answer_correct_format = False
    attempt = 0
    while not answer_correct_format:
        answer = user_proxy.last_message(agent)["content"]
        json_answer = from_string_to_json(answer)

        if all(key.lower() in map(str.lower, json_answer) for key in ["Comment"]) and len(json_answer) == 1 and all(isinstance(value, str) for value in json_answer.values()):
            answer_correct_format = True
        else:
            attempt += 1
            if attempt <= 3:
                user_proxy.initiate_chat(
                    agent,
                    message=read_from_file("check_conversation_1_to_1_format", "Prompt/errors"),
                    clear_history=False
                )
            else:
                answer_correct_format = True
                json_answer = {
                    "Choice": "2",
                    "Reason": "Auto",
                    "New content": "N/A"
                }
    return json_answer


def check_follow_content_format(user_proxy, agent):
    answer_correct_format = False
    attempt = 0
    while not answer_correct_format:
        answer = user_proxy.last_message(agent)["content"]
        json_answer = from_string_to_json(answer)

        if all(key.lower() in map(str.lower, json_answer) for key in ["Followed user"]) and len(json_answer) == 1 and all(isinstance(value, str) for value in json_answer.values()):
            answer_correct_format = True
        else:
            attempt += 1
            if attempt <= 3:
                user_proxy.initiate_chat(
                    agent,
                    message=read_from_file("check_follow_content_format", "Prompt/errors"),
                    clear_history=False
                )
            else:
                answer_correct_format = True
                json_answer = {
                    "Choice": "2",
                    "Reason": "Auto",
                    "New content": "N/A"
                }
    return json_answer


def check_interview_format(user_proxy, agent):
    answer_correct_format = False
    attempt = 0
    while not answer_correct_format:
        answer = user_proxy.last_message(agent)["content"]
        json_answer = from_string_to_json(answer)

        if all(key.lower() in map(str.lower, json_answer) for key in ["Main Influence", "Explanation"]) and len(json_answer) == 2 and all(isinstance(value, str) for value in json_answer.values()):
            answer_correct_format = True
        else:
            attempt += 1
            if attempt <= 3:
                user_proxy.initiate_chat(
                    agent,
                    message=read_from_file("check_interview_format", "Prompt/errors"),
                    clear_history=False
                )
            else:
                answer_correct_format = True
                json_answer = {
                    "Choice": "2",
                    "Reason": "Auto",
                    "New content": "N/A"
                }
    return json_answer


# FUNCTIONS FOR CALCULATING EMBEDDINGS AND SIMILARITY
def get_embedding(text):
    return model.encode(text)


def calculate_similarity(embedding1, embedding2):
    return cosine_similarity([embedding1], [embedding2])[0][0]
