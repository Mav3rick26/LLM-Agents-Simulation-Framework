from utils import *
from agents import user_proxy, agent_list, personality_folder
from prompts import *
from short_term_memory import *
from long_term_memory import *
from recsys import search_recommended_contents
from sentiment_analysis_utility import perform_sentiment_analysis
from friends_network import *
from output import save_to_csv, get_memory_data
from resume_sim import *
from simulation_saturation import compute_simulation_saturation

NUM_MAX_ITERATIONS = 4
current_iteration = get_iteration()

SHARE_VIRALITY_SCORE = 1
LIKE_SENTIMENT_SCORE = 1
DISLIKE_SENTIMENT_SCORE = -1
EMBEDDING_SIMILARITY_THRESHOLD = 0.99

choice = ""
content = ""
answer = ""
main_influence = ""
explanation = ""
json_answer = {}

agent_personality = ""

actions_dict = []
comments_dict = []
connections_dict = []
interviews_dict = []

# Resume simulation
if current_iteration != 0:
    load_friends_network('Output/connections_log.csv', agent_list)
    actions_dict = load_actions_dict('Output/simulation_log.csv')
    comments_dict = load_comments_dict('Output/comments_log.csv')
    connections_dict = load_connections_dict('Output/connections_log.csv')
    interviews_dict = load_interviews_dict('Output/interviews_log.csv')
    clear_stm()
    load_stm('Output/stm.csv')
    clear_ltm()
    load_ltm('Output/ltm.csv')

res_stm = get_stm()
print(res_stm)

res_ltm = get_ltm()
print(res_ltm)

# Simulation loop
for iteration in range(current_iteration, NUM_MAX_ITERATIONS):
    num_agent = 0

    for agent in agent_list:
        num_agent += 1
        num_iteration = iteration + 1
        print(f"Iteration {num_iteration} - Agent {num_agent}")
        risposta_stm = get_feedbacks_from_stm(agent)
        risposta_ltm = get_feedbacks_from_ltm(agent)

        full_prompt = ""
        feedbacks_prompt = ""
        related_content_string = ""
        feedbacks_string = ""
        agent_follows_list = get_follow_list(agent)
        agent_followers_list = get_follower_list(agent)
        at_least_one_follow = False
        at_least_one_follower = False

        # PHASE 0 - Follow another agent
        if iteration != 0 and any(action['Agent'] == agent.name and action['Choice'] == 'Posting new content' for action in actions_dict):
            suggested_follow_list = get_suggested_follow_list(agent, agent_list, agent_follows_list)
            suggested_follow_string = suggested_follows_to_string(suggested_follow_list, personality_folder)
            choice_7_prompt = follow_prompt_part_1 + "\n" + suggested_follow_string + follow_prompt_part_2

            user_proxy.initiate_chat(
                agent,
                message=choice_7_prompt
            )

            json_answer = check_follow_content_format(user_proxy, agent)
            json_answer_lower = {key.lower(): value for key, value in json_answer.items()}

            agent_to_follow = json_answer_lower.get("followed user", "")

            if agent_to_follow != "N/A":
                is_agent_followed = False
                for selected_agent in agent_list:
                    if selected_agent.name.lower() == agent_to_follow.lower():
                        is_agent_followed = add_follow(agent, selected_agent)
                        if is_agent_followed:
                            connections_dict.append({
                                'Iteration': num_iteration,
                                'Agent': agent.name,
                                'Followed Agent': selected_agent.name
                            })
                        break

                attempt = 1
                while not is_agent_followed and attempt < 3:
                    user_proxy.initiate_chat(
                        agent,
                        message=follow_user_not_found_error_part_1 + "\n" + suggested_follow_string + "\n" + follow_user_not_found_error_part_2
                    )

                    for selected_agent in agent_list:
                        if selected_agent.name.lower() == agent_to_follow.lower():
                            is_agent_followed = add_follow(agent, selected_agent)
                            if is_agent_followed:
                                connections_dict.append({
                                    'Iteration': num_iteration,
                                    'Agent': agent.name,
                                    'Followed Agent': selected_agent.name
                                })
                            break

                    attempt += 1

        # PHASE 1 - Inferencing Choice and Reason
        if iteration == 0:
            full_prompt = main_prompt_zero_follows
        else:
            agent_personality = read_from_file(f"{agent.name.lower()}.txt", personality_folder)
            agent_follows_list = get_follow_list(agent)
            agent_followers_list = get_follower_list(agent)
            if len(agent_followers_list) != 0:
                at_least_one_follower = True
                stm_feedbacks = get_feedbacks_from_stm(agent)
                ltm_feedbacks = get_feedbacks_from_ltm(agent)
                feedbacks_string = stm_feedbacks + "\n" + ltm_feedbacks
                feedbacks_prompt = feedbacks_prompt_part_1 + "\n" + feedbacks_string + "\n" + feedbacks_prompt_part_2

            if len(agent_follows_list) != 0:
                related_content = search_recommended_contents(agent_personality, agent_follows_list)
                if related_content is not None:
                    at_least_one_follow = True
                    related_content_list = get_unique_contents(related_content)
                    related_content_string = related_contents_to_string(related_content_list).rstrip('\n')

            if at_least_one_follower and at_least_one_follow:
                full_prompt = feedbacks_prompt + "\n\n" + main_prompt_part_1 + "\n" + related_content_string + "\n" + main_prompt_part_2
            elif not at_least_one_follower and at_least_one_follow:
                full_prompt = main_prompt_part_1 + "\n" + related_content_string + "\n" + main_prompt_part_2
            elif at_least_one_follower and not at_least_one_follow:
                full_prompt = feedbacks_prompt + "\n\n" + main_prompt_zero_follows
            elif not at_least_one_follower and not at_least_one_follow:
                full_prompt = main_prompt_zero_follows

        user_proxy.initiate_chat(
            agent,
            message=full_prompt
        )

        json_answer = check_choice_reason_format(user_proxy, agent)
        json_answer_lower = {key.lower(): value for key, value in json_answer.items()}

        choice = int(json_answer_lower.get("choice", "").strip('"'))
        reason = json_answer_lower.get("reason", "")

        # PHASE 2 - Inferencing basing on the Choice
        end_conversation = False
        attempt = 0
        while not end_conversation:
            if choice == 1:  # Posting new content
                choice_1_prompt = choice_1_prompt_part_1 + "\n" + reason + "\n" + choice_1_prompt_part_2

                user_proxy.initiate_chat(
                    agent,
                    message=choice_1_prompt
                )

                json_answer = check_new_content_format(user_proxy, agent)
                json_answer_lower = {key.lower(): value for key, value in json_answer.items()}

                content = json_answer_lower.get("new content", "")

                if content != "N/A":
                    add_content_to_stm(agent, content, 0, 0, iteration)

                    end_conversation = True
                    actions_dict.append({
                        'Iteration': num_iteration,
                        'Agent': agent.name,
                        'Choice': 'Posting new content',
                        'Reason': reason,
                        'Content': content
                    })
                else:
                    choice = 2
                    reason = "Auto"
            elif choice == 2:  # Not interacting
                end_conversation = True
                actions_dict.append({
                    'Iteration': num_iteration,
                    'Agent': agent.name,
                    'Choice': 'Not interacting',
                    'Reason': reason,
                    'Content': "N/A"
                })
            elif choice == 3 and at_least_one_follow:  # Sharing content
                choice_3_prompt = choice_3_prompt_part_1 + "\n" + reason + "\n" + choice_3_prompt_part_2 + "\n" + related_content_string + "\n" + choice_3_prompt_part_3

                user_proxy.initiate_chat(
                    agent,
                    message=choice_3_prompt
                )

                json_answer = check_shared_content_format(user_proxy, agent)
                json_answer_lower = {key.lower(): value for key, value in json_answer.items()}

                content = json_answer_lower.get("shared content", "")

                shared_content_id_index = [i for i, value in enumerate(related_content['documents'][0]) if calculate_similarity(get_embedding(value), get_embedding(content)) > EMBEDDING_SIMILARITY_THRESHOLD]
                if len(shared_content_id_index) <= 0:  # Error Handling
                    attempt += 1
                    if attempt <= 3:
                        user_proxy.initiate_chat(
                            agent,
                            message=choice_3_content_not_found_error_part_1 + "\n" + related_content_string + "\n" + choice_3_content_not_found_error_part_2
                        )

                        json_answer = check_shared_content_format(user_proxy, agent)
                        json_answer_lower = {key.lower(): value for key, value in json_answer.items()}

                        content = json_answer_lower.get("shared content", "")

                        shared_content_id_index = [i for i, value in enumerate(related_content['documents'][0]) if value == content]  # Filtra gli indici degli elementi uguali al content condiviso dall'agente
                    else:
                        choice = 2
                        reason = "Auto"
                else:
                    source_agent_id = related_content['ids'][0][shared_content_id_index[-1]]
                    if is_content_in_stm(source_agent_id):
                        modify_stm_virality_score(source_agent_id, SHARE_VIRALITY_SCORE)
                        evaluate_stm_content_for_ltm_transfer(source_agent_id)
                    elif is_content_in_ltm(source_agent_id):
                        modify_ltm_virality_score(source_agent_id, SHARE_VIRALITY_SCORE)

                    end_conversation = True
                    actions_dict.append({
                        'Iteration': num_iteration,
                        'Agent': agent.name,
                        'Choice': 'Sharing content',
                        'Reason': reason,
                        'Content': content
                    })
            elif choice == 4 and at_least_one_follow:  # Liking content
                choice_4_prompt = choice_4_prompt_part_1 + "\n" + reason + "\n" + choice_4_prompt_part_2 + "\n" + related_content_string + "\n" + choice_4_prompt_part_3

                user_proxy.initiate_chat(
                    agent,
                    message=choice_4_prompt
                )

                json_answer = check_liked_content_format(user_proxy, agent)
                json_answer_lower = {key.lower(): value for key, value in json_answer.items()}

                content = json_answer_lower.get("liked content", "")

                shared_content_id_index = [i for i, value in enumerate(related_content['documents'][0]) if calculate_similarity(get_embedding(value), get_embedding(content)) > EMBEDDING_SIMILARITY_THRESHOLD]
                if len(shared_content_id_index) <= 0:  # Error Handling
                    attempt += 1
                    if attempt <= 3:
                        user_proxy.initiate_chat(
                            agent,
                            message=choice_4_content_not_found_error_part_1 + "\n" + related_content_string + "\n" + choice_4_content_not_found_error_part_2
                        )

                        json_answer = check_liked_content_format(user_proxy, agent)
                        json_answer_lower = {key.lower(): value for key, value in json_answer.items()}

                        content = json_answer_lower.get("liked content", "")

                        shared_content_id_index = [i for i, value in enumerate(related_content['documents'][0]) if value == content]  # Filtra gli indici degli elementi uguali al content condiviso dall'agente
                    else:
                        choice = 2
                        reason = "Auto"
                else:
                    source_agent_id = related_content['ids'][0][shared_content_id_index[-1]]
                    if is_content_in_stm(source_agent_id):
                        modify_stm_sentiment_score(source_agent_id, LIKE_SENTIMENT_SCORE)
                        evaluate_stm_content_for_ltm_transfer(source_agent_id)
                    elif is_content_in_ltm(source_agent_id):
                        modify_ltm_sentiment_score(source_agent_id, LIKE_SENTIMENT_SCORE)

                    end_conversation = True
                    actions_dict.append({
                        'Iteration': num_iteration,
                        'Agent': agent.name,
                        'Choice': 'Liking content',
                        'Reason': reason,
                        'Content': content
                    })
            elif choice == 5 and at_least_one_follow:  # Disliking content
                choice_5_prompt = choice_5_prompt_part_1 + "\n" + reason + "\n" + choice_5_prompt_part_2 + "\n" + related_content_string + "\n" + choice_5_prompt_part_3

                user_proxy.initiate_chat(
                    agent,
                    message=choice_5_prompt
                )

                json_answer = check_disliked_content_format(user_proxy, agent)
                json_answer_lower = {key.lower(): value for key, value in json_answer.items()}

                content = json_answer_lower.get("disliked content", "")

                shared_content_id_index = [i for i, value in enumerate(related_content['documents'][0]) if calculate_similarity(get_embedding(value), get_embedding(content)) > EMBEDDING_SIMILARITY_THRESHOLD]
                if len(shared_content_id_index) <= 0:  # Error Handling
                    attempt += 1
                    if attempt <= 3:
                        user_proxy.initiate_chat(
                            agent,
                            message=choice_5_content_not_found_error_part_1 + "\n" + related_content_string + "\n" + choice_5_content_not_found_error_part_2
                        )

                        json_answer = check_disliked_content_format(user_proxy, agent)
                        json_answer_lower = {key.lower(): value for key, value in json_answer.items()}

                        content = json_answer_lower.get("disliked content", "")

                        shared_content_id_index = [i for i, value in enumerate(related_content['documents'][0]) if value == content]  # Filtra gli indici degli elementi uguali al content condiviso dall'agente
                    else:
                        choice = 2
                        reason = "Auto"
                else:
                    source_agent_id = related_content['ids'][0][shared_content_id_index[-1]]
                    if is_content_in_stm(source_agent_id):
                        modify_stm_sentiment_score(source_agent_id, DISLIKE_SENTIMENT_SCORE)
                        evaluate_stm_content_for_ltm_transfer(source_agent_id)
                    elif is_content_in_ltm(source_agent_id):
                        modify_ltm_sentiment_score(source_agent_id, DISLIKE_SENTIMENT_SCORE)

                    end_conversation = True
                    actions_dict.append({
                        'Iteration': num_iteration,
                        'Agent': agent.name,
                        'Choice': 'Disliking content',
                        'Reason': reason,
                        'Content': content
                    })
            elif choice == 6 and at_least_one_follow:  # Commenting content
                choice_6_prompt = choice_6_prompt_part_1 + "\n" + reason + "\n" + choice_6_prompt_part_2 + "\n" + related_content_string + "\n" + choice_6_prompt_part_3

                user_proxy.initiate_chat(
                    agent,
                    message=choice_6_prompt
                )

                json_answer = check_commented_content_format(user_proxy, agent)
                json_answer_lower = {key.lower(): value for key, value in json_answer.items()}

                content = json_answer_lower.get("commented content", "")

                shared_content_id_index = [i for i, value in enumerate(related_content['documents'][0]) if calculate_similarity(get_embedding(value), get_embedding(content)) > EMBEDDING_SIMILARITY_THRESHOLD]
                if len(shared_content_id_index) <= 0:  # Error Handling
                    attempt += 1
                    if attempt <= 3:
                        user_proxy.initiate_chat(
                            agent,
                            message=choice_6_content_not_found_error_part_1 + "\n" + related_content_string + "\n" + choice_6_content_not_found_error_part_2
                        )

                        json_answer = check_commented_content_format(user_proxy, agent)
                        json_answer_lower = {key.lower(): value for key, value in json_answer.items()}

                        content = json_answer_lower.get("commented content", "")

                        shared_content_id_index = [i for i, value in enumerate(related_content['documents'][0]) if value == content]  # Filtra gli indici degli elementi uguali al content condiviso dall'agente
                    else:
                        choice = 2
                        reason = "Auto"
                else:
                    comment_history = []
                    comment_history_string = ""
                    source_agent = ""
                    source_agent_id = related_content['ids'][0][shared_content_id_index[-1]]
                    if is_content_in_stm(source_agent_id):
                        source_agent_string = get_source_agent_from_stm(source_agent_id)
                        source_agent = get_agent_from_agent_list(agent_list, source_agent_string)
                        choice_6_prompt_get_comment = choice_6_prompt_part_4 + "\n" + content + "\n" + choice_6_prompt_part_5

                        user_proxy.initiate_chat(
                            agent,
                            message=choice_6_prompt_get_comment
                        )

                        json_answer = check_conversation_1_to_1_format(user_proxy, agent)
                        json_answer_lower = {key.lower(): value for key, value in json_answer.items()}

                        comment = json_answer_lower.get("comment", "")

                        end_1_to_1_conversation = False
                        comment_history = [comment]
                        sentiment_value = perform_sentiment_analysis(comment)
                        sentiment_list = [sentiment_value]
                        num_comment = 1
                        while not end_1_to_1_conversation and num_comment <= 6:
                            comment_history_string = ""
                            for comment in comment_history:
                                comment_history_string += comment + "\n"

                            one_to_one_prompt_source_agent = one_to_one_prompt_part_1 + "\n" + content + "\n" + one_to_one_prompt_part_2 + "\n" + comment_history_string + one_to_one_prompt_part_3

                            user_proxy.initiate_chat(
                                source_agent,
                                message=one_to_one_prompt_source_agent
                            )

                            comment = user_proxy.last_message(source_agent)["content"]

                            if "End conversation" in comment:
                                end_1_to_1_conversation = True
                            else:
                                comment_history.append(comment)
                                num_comment += 1

                                comment_history_string = ""
                                for comment in comment_history:
                                    comment_history_string += "\"" + comment + "\"\n"

                                one_to_one_prompt_commenting_agent = one_to_one_prompt_part_4 + "\n" + content + "\n" + one_to_one_prompt_part_5 + "\n" + comment_history_string + one_to_one_prompt_part_6

                                user_proxy.initiate_chat(
                                    agent,
                                    message=one_to_one_prompt_commenting_agent
                                )

                                comment = user_proxy.last_message(agent)["content"]

                                if "End conversation" in comment:
                                    end_1_to_1_conversation = True
                                else:
                                    comment_history.append(comment)
                                    sentiment_value = perform_sentiment_analysis(comment)
                                    sentiment_list.append(sentiment_value)
                                    num_comment += 1

                        average_sentiment = sum(sentiment_list) / len(sentiment_list) if sentiment_list else 0
                        modify_stm_sentiment_score(source_agent_id, average_sentiment)
                        evaluate_stm_content_for_ltm_transfer(source_agent_id)
                    elif is_content_in_ltm(source_agent_id):
                        source_agent_string = get_source_agent_from_ltm(source_agent_id)
                        source_agent = get_agent_from_agent_list(agent_list, source_agent_string)
                        choice_6_prompt_get_comment = choice_6_prompt_part_4 + "\n" + content + "\n" + choice_6_prompt_part_5

                        user_proxy.initiate_chat(
                            agent,
                            message=choice_6_prompt_get_comment
                        )

                        json_answer = check_conversation_1_to_1_format(user_proxy, agent)
                        json_answer_lower = {key.lower(): value for key, value in json_answer.items()}

                        comment = json_answer_lower.get("comment", "")

                        end_1_to_1_conversation = False
                        comment_history = [comment]
                        sentiment_value = perform_sentiment_analysis(comment)
                        sentiment_list = [sentiment_value]
                        num_comment = 1
                        while not end_1_to_1_conversation and num_comment <= 6:
                            comment_history_string = ""
                            for comment in comment_history:
                                comment_history_string += comment + "\n"

                            one_to_one_prompt_source_agent = one_to_one_prompt_part_1 + "\n" + content + "\n" + one_to_one_prompt_part_2 + "\n" + comment_history_string + one_to_one_prompt_part_3

                            user_proxy.initiate_chat(
                                source_agent,
                                message=one_to_one_prompt_source_agent
                            )

                            comment = user_proxy.last_message(source_agent)["content"]

                            if "End conversation" in comment:
                                end_1_to_1_conversation = True
                            else:
                                comment_history.append(comment)
                                num_comment += 1

                                comment_history_string = ""
                                for comment in comment_history:
                                    comment_history_string += "\"" + comment + "\"\n"

                                one_to_one_prompt_commenting_agent = one_to_one_prompt_part_4 + "\n" + content + "\n" + one_to_one_prompt_part_5 + "\n" + comment_history_string + one_to_one_prompt_part_6

                                user_proxy.initiate_chat(
                                    agent,
                                    message=one_to_one_prompt_commenting_agent
                                )

                                comment = user_proxy.last_message(agent)["content"]

                                if "End conversation" in comment:
                                    end_1_to_1_conversation = True
                                else:
                                    comment_history.append(comment)
                                    sentiment_value = perform_sentiment_analysis(comment)
                                    sentiment_list.append(sentiment_value)
                                    num_comment += 1

                        average_sentiment = sum(sentiment_list) / len(sentiment_list) if sentiment_list else 0
                        modify_ltm_sentiment_score(source_agent_id, average_sentiment)

                    end_conversation = True
                    actions_dict.append({
                        'Iteration': num_iteration,
                        'Agent': agent.name,
                        'Choice': 'Commenting content',
                        'Reason': reason,
                        'Content': content
                    })

                    comments_dict.append({
                        'Iteration': num_iteration,
                        'Commenting Agent': agent.name,
                        'Source Agent': source_agent.name,
                        'Content': content,
                        'Comment History': comment_history_string,
                        'Number of Comments': len(comment_history)
                    })
            else:
                choice = 2
                reason = "Auto"

        # PHASE 3 - Agent interview
        interview_prompt = ""
        if iteration != 0 and reason != "Auto" and at_least_one_follower:
            if choice == 1:
                interview_prompt = agent_interview_choice_1_part_1 + "\n" + feedbacks_string + agent_interview_choice_1_part_2 + "\n" + content + "\n" + agent_interview_choice_1_part_3
            elif choice == 2:
                interview_prompt = agent_interview_choice_2_part_1 + "\n" + feedbacks_string + agent_interview_choice_2_part_2
            elif choice == 3:
                interview_prompt = agent_interview_choice_3_part_1 + "\n" + feedbacks_string + agent_interview_choice_3_part_2 + "\n" + content + "\n" + agent_interview_choice_3_part_3
            elif choice == 4:
                interview_prompt = agent_interview_choice_4_part_1 + "\n" + feedbacks_string + agent_interview_choice_4_part_2 + "\n" + content + "\n" + agent_interview_choice_4_part_3
            elif choice == 5:
                interview_prompt = agent_interview_choice_5_part_1 + "\n" + feedbacks_string + agent_interview_choice_5_part_2 + "\n" + content + "\n" + agent_interview_choice_5_part_3
            elif choice == 6:
                interview_prompt = agent_interview_choice_6_part_1 + "\n" + feedbacks_string + agent_interview_choice_6_part_2 + "\n" + content + "\n" + agent_interview_choice_6_part_3

            user_proxy.initiate_chat(
                agent,
                message=interview_prompt
            )

            json_answer = check_interview_format(user_proxy, agent)
            json_answer_lower = {key.lower(): value for key, value in json_answer.items()}

            main_influence = json_answer_lower.get("main influence", "")
            explanation = json_answer_lower.get("explanation", "")

            interviews_dict.append({
                'Iteration': num_iteration,
                'Agent': agent.name,
                'Main Influence': main_influence,
                'Explanation': explanation
            })

    # ITERATION ENDING
    content_score_decadency_law_stm(iteration)

    # SIMULATION ENDING - Simulation output
    if iteration != 0:
        # Logs all actions taken during the simulation, including choices made by agents
        save_to_csv(actions_dict, 'simulation_log')

        # Logs all comments made by agents on content during the simulation
        save_to_csv(comments_dict, 'comments_log')

        # Logs all follow connections made between agents during the simulation
        save_to_csv(connections_dict, 'connections_log')
        followed_count = pd.DataFrame(connections_dict)['Followed Agent'].value_counts().reset_index()  # Count how many times each agent appears in the "Followed Agent" column of the connections DataFrame
        followed_count.columns = ['Agent', 'Follower']
        followed_count.to_csv('Output/followed_agents_count.csv', index=False)

        # Logs all short-term and long-term memory data
        stm_data = get_memory_data(get_stm())
        ltm_data = get_memory_data(get_ltm())
        save_to_csv(stm_data, 'stm')
        save_to_csv(ltm_data, 'ltm')

        # Logs all interviews made by agents during the simulation
        save_to_csv(interviews_dict, 'interviews_log')

    if iteration == NUM_MAX_ITERATIONS - 1:
        compute_simulation_saturation(NUM_MAX_ITERATIONS)
