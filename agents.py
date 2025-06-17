import autogen
import os
import pandas as pd
from utils import llama3, read_from_file, save_personality_to_file

# Dataset switcher
usa_election = False
qanon = False
brexit = False
personas = True

user_proxy = autogen.UserProxyAgent(
    name="user_proxy",
    human_input_mode="NEVER",
    max_consecutive_auto_reply=0,
    code_execution_config=False,
    default_auto_reply="default_auto_reply"
)

assistant = autogen.AssistantAgent(
    name="assistant",
    system_message="You are a sociologist.",
    llm_config=llama3
)

agent_list = []
dataset_folder = ""
personality_folder = ""
behavioral_folder = ""

if usa_election:
    dataset_folder = "Dataset/USA_Election"
    personality_folder = "Personalities/USA_Election"

    NUM_DEMOCRATICS = 2  # 27
    NUM_REPUBLICANS = 2  # 73

    df_democratics = pd.read_csv(f'{dataset_folder}/Democratics.csv', encoding='utf-8')
    democratic_users = df_democratics['User'].unique()  # 205 users (27%)

    df_republicans = pd.read_csv(f'{dataset_folder}/Republicans.csv', encoding='utf-8')
    republican_users = df_republicans['User'].unique()  # 543 users (73%)

    df_original_tweets = pd.read_csv(f'{dataset_folder}/Original_Tweets.csv', encoding='utf-8')

    users = []

    for i in range(max(NUM_DEMOCRATICS, NUM_REPUBLICANS)):
        if i < NUM_DEMOCRATICS:
            users.append(democratic_users[i])
        if i < NUM_REPUBLICANS:
            users.append(republican_users[i])

    for index, user in enumerate(users, start=1):
        if not os.path.exists(f"{personality_folder}/{user.lower()}.txt"):
            print(f'Agent {index}')
            user_tweet = df_original_tweets[df_original_tweets['User'] == user]['Tweet'].head(30)  # Filter the DataFrame for the user of interest and select the 'Tweet' column
            user_tweet_string = '\n'.join(user_tweet)  # Create a single string with '\n' at the end of each tweet

            task_for_personality = f"""These are contents published by {user} on a social network:\n{user_tweet_string}\n\nDescribe {user}'s personality in 30 words basing on these contents using sentences like "You are..."."""

            user_proxy.initiate_chat(
                assistant,
                message=task_for_personality
            )

            # Save agent's personality
            save_personality_to_file(user_proxy.last_message()["content"], str(user.lower()), folder=personality_folder)

        agent_personality = read_from_file(f"{user.lower()}.txt", personality_folder)

        agent = autogen.AssistantAgent(
            name=f"{user}",
            system_message=f"You are {user}. {agent_personality} You are tasked with making a decision about your activity on a social network based on feedback received on your previous posts and related content from other users.",
            llm_config=llama3,
        )

        agent_list.append(agent)


elif personas:
    personality_folder = "Personalities/personas_980"
    behavioral_folder = "behavior_profiles"
    
    for filename in os.listdir(personality_folder):
        if filename.endswith(".txt"):
            agent_name = filename.replace(".txt", "")
            agent_personality = read_from_file(filename, folder=personality_folder)

            agent = autogen.AssistantAgent(
                name=agent_name,
                system_message=agent_personality,
                llm_config=llama3,
            )
            agent_list.append(agent)


elif qanon:
    dataset_folder = "Dataset/QAnon"
    personality_folder = "Personalities/QAnon"

    df = pd.read_csv(f'{dataset_folder}/QAnon_tweets.csv', encoding='latin1')
    unique_users = df['from_user'].unique()[:100]  # Get the first 100 unique users
    df_original_tweets = df[['from_user', 'text']]  # Extract original tweets
    users = list(unique_users)

    for index, user in enumerate(users, start=1):
        if not os.path.exists(f"{personality_folder}/{user.lower()}.txt"):
            print(f'Agent {index}')
            user_tweet = df_original_tweets[df_original_tweets['from_user'] == user]['text'].head(30)  # Filter the DataFrame for the user of interest and select the 'text' column
            user_tweet_string = '\n'.join(user_tweet)  # Create a single string with '\n' at the end of each tweet

            task_for_personality = f"""These are contents published by {user} on a social network:\n{user_tweet_string}\n\nDescribe {user}'s personality in 30 words basing on these contents using sentences like "You are..."."""

            user_proxy.initiate_chat(
                assistant,
                message=task_for_personality
            )

            # Save agent's personality
            save_personality_to_file(user_proxy.last_message()["content"], str(user.lower()), personality_folder)

        agent_personality = read_from_file(f"{user.lower()}.txt", personality_folder)

        agent = autogen.AssistantAgent(
            name=f"{user}",
            system_message=f"You are {user}. {agent_personality} You are tasked with making a decision about your activity on a social network based on feedback received on your previous posts and related content from other users.",
            llm_config=llama3,
        )

        agent_list.append(agent)

elif brexit:
    dataset_folder = "Dataset/Brexit"
    personality_folder = "Personalities/Brexit"

    NUM_ANTI_BREXIT = 55  # 55
    NUM_PRO_BREXIT = 45  # 45

    df_anti_brexit = pd.read_csv(f'{dataset_folder}/Anti_Brexit_Users.csv', encoding='utf-8')
    anti_brexit_users = df_anti_brexit['User'].unique()  # 2490 users (55%)

    df_pro_brexit = pd.read_csv(f'{dataset_folder}/Pro_Brexit_Users.csv', encoding='utf-8')
    pro_brexit_users = df_pro_brexit['User'].unique()  # 2037 users (45%)

    df_original_tweets = pd.read_csv(f'{dataset_folder}/User_Tweet.csv', encoding='utf-8')

    users = []

    for i in range(max(NUM_ANTI_BREXIT, NUM_PRO_BREXIT)):
        if i < NUM_ANTI_BREXIT:
            users.append(anti_brexit_users[i])
        if i < NUM_PRO_BREXIT:
            users.append(pro_brexit_users[i])

    for index, user in enumerate(users, start=1):
        if not os.path.exists(f"{personality_folder}/{user.lower()}.txt"):
            print(f'Agent {index}')
            user_tweet = df_original_tweets[df_original_tweets['User'] == user]['Tweet'].head(30)  # Filter the DataFrame for the user of interest and select the 'Tweet' column
            user_tweet_string = '\n'.join(user_tweet)  # Create a single string with '\n' at the end of each tweet

            task_for_personality = f"""These are contents published by {user} on a social network:\n{user_tweet_string}\n\nDescribe {user}'s personality in 30 words basing on these contents using sentences like "You are..."."""

            user_proxy.initiate_chat(
                assistant,
                message=task_for_personality
            )

            # Save agent's personality
            save_personality_to_file(user_proxy.last_message()["content"], str(user.lower()), folder=personality_folder)

        agent_personality = read_from_file(f"{user.lower()}.txt", personality_folder)

        agent = autogen.AssistantAgent(
            name=f"{user}",
            system_message=f"You are {user}. {agent_personality} You are tasked with making a decision about your activity on a social network based on feedback received on your previous posts and related content from other users.",
            llm_config=llama3,
        )

        agent_list.append(agent)
