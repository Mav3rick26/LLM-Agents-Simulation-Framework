from utils import read_from_file
from short_term_activity_memory import get_activity

# INITIAL PROMPTS #
main_prompt_zero_follows = read_from_file("main_prompt_zero_follows", "Prompt/main_prompts")
main_prompt_part_1 = read_from_file("main_prompt_part_1", "Prompt/main_prompts")
main_prompt_part_2 = read_from_file("main_prompt_part_2", "Prompt/main_prompts")

feedbacks_prompt_part_1 = read_from_file("feedbacks_prompt_part_1", "Prompt/main_prompts")
feedbacks_prompt_part_2 = read_from_file("feedbacks_prompt_part_2", "Prompt/main_prompts")

# --------- #

# NEW CONTENT #
choice_1_prompt_part_1 = read_from_file("choice_1_prompt_part_1", "Prompt/choice_1_prompts_new_content")
choice_1_prompt_part_2 = read_from_file("choice_1_prompt_part_2", "Prompt/choice_1_prompts_new_content")

# --------- #

# SHARE CONTENT #
choice_3_prompt_part_1 = read_from_file("choice_3_prompt_part_1", "Prompt/choice_3_prompts_share")
choice_3_prompt_part_2 = read_from_file("choice_3_prompt_part_2", "Prompt/choice_3_prompts_share")
choice_3_prompt_part_3 = read_from_file("choice_3_prompt_part_3", "Prompt/choice_3_prompts_share")

# Errors
choice_3_content_not_found_error_part_1 = read_from_file("choice_3_content_not_found_error_part 1", "Prompt/choice_3_prompts_share/errors")
choice_3_content_not_found_error_part_2 = read_from_file("choice_3_content_not_found_error_part_2", "Prompt/choice_3_prompts_share/errors")

# --------- #

# LIKE CONTENT #
choice_4_prompt_part_1 = read_from_file("choice_4_prompt_part_1", "Prompt/choice_4_prompts_like")
choice_4_prompt_part_2 = read_from_file("choice_4_prompt_part_2", "Prompt/choice_4_prompts_like")
choice_4_prompt_part_3 = read_from_file("choice_4_prompt_part_3", "Prompt/choice_4_prompts_like")

# Errors
choice_4_content_not_found_error_part_1 = read_from_file("choice_4_content_not_found_error_part 1", "Prompt/choice_4_prompts_like/errors")
choice_4_content_not_found_error_part_2 = read_from_file("choice_4_content_not_found_error_part_2", "Prompt/choice_4_prompts_like/errors")

# --------- #

# DISLIKE CONTENT #
choice_5_prompt_part_1 = read_from_file("choice_5_prompt_part_1", "Prompt/choice_5_prompts_dislike")
choice_5_prompt_part_2 = read_from_file("choice_5_prompt_part_2", "Prompt/choice_5_prompts_dislike")
choice_5_prompt_part_3 = read_from_file("choice_5_prompt_part_3", "Prompt/choice_5_prompts_dislike")

# Errors
choice_5_content_not_found_error_part_1 = read_from_file("choice_5_content_not_found_error_part 1", "Prompt/choice_5_prompts_dislike/errors")
choice_5_content_not_found_error_part_2 = read_from_file("choice_5_content_not_found_error_part_2", "Prompt/choice_5_prompts_dislike/errors")

# --------- #

# COMMENT CONTENT #
choice_6_prompt_part_1 = read_from_file("choice_6_prompt_part_1", "Prompt/choice_6_prompts_comment")
choice_6_prompt_part_2 = read_from_file("choice_6_prompt_part_2", "Prompt/choice_6_prompts_comment")
choice_6_prompt_part_3 = read_from_file("choice_6_prompt_part_3", "Prompt/choice_6_prompts_comment")
choice_6_prompt_part_4 = read_from_file("choice_6_prompt_part_4", "Prompt/choice_6_prompts_comment")
choice_6_prompt_part_5 = read_from_file("choice_6_prompt_part_5", "Prompt/choice_6_prompts_comment")

# One-to-one conversation source agent prompts
one_to_one_prompt_part_1 = read_from_file("one_to_one_prompt_part_1", "Prompt/choice_6_prompts_comment")
one_to_one_prompt_part_2 = read_from_file("one_to_one_prompt_part_2", "Prompt/choice_6_prompts_comment")
one_to_one_prompt_part_3 = read_from_file("one_to_one_prompt_part_3", "Prompt/choice_6_prompts_comment")

# One-to-one conversation commenting agent prompts
one_to_one_prompt_part_4 = read_from_file("one_to_one_prompt_part_4", "Prompt/choice_6_prompts_comment")
one_to_one_prompt_part_5 = read_from_file("one_to_one_prompt_part_5", "Prompt/choice_6_prompts_comment")
one_to_one_prompt_part_6 = read_from_file("one_to_one_prompt_part_6", "Prompt/choice_6_prompts_comment")

# Errors
choice_6_content_not_found_error_part_1 = read_from_file("choice_6_content_not_found_error_part 1", "Prompt/choice_6_prompts_comment/errors")
choice_6_content_not_found_error_part_2 = read_from_file("choice_6_content_not_found_error_part_2", "Prompt/choice_6_prompts_comment/errors")

# --------- #

# ADD FOLLOW #
follow_prompt_part_1 = read_from_file("follow_prompt_part_1", "Prompt/follow_prompts")
follow_prompt_part_2 = read_from_file("follow_prompt_part_2", "Prompt/follow_prompts")

# Errors
follow_user_not_found_error_part_1 = read_from_file("follow_user_not_found_error_part_1", "Prompt/follow_prompts/errors")
follow_user_not_found_error_part_2 = read_from_file("follow_user_not_found_error_part_2", "Prompt/follow_prompts/errors")

# --------- #

# GENERAL ERRORS #
answer_incorrect_format = read_from_file("answer_incorrect_format", "Prompt/errors")

# --------- #

# AGENT INTERVIEW #
# Choice 1
agent_interview_choice_1_part_1 = read_from_file("agent_interview_prompt_choice_1_part_1", "Prompt/choice_1_prompts_new_content")
agent_interview_choice_1_part_2 = read_from_file("agent_interview_prompt_choice_1_part_2", "Prompt/choice_1_prompts_new_content")
agent_interview_choice_1_part_3 = read_from_file("agent_interview_prompt_choice_1_part_3", "Prompt/choice_1_prompts_new_content")

# Choice 2
agent_interview_choice_2_part_1 = read_from_file("agent_interview_prompt_choice_2_part_1", "Prompt/choice_2_prompts_no_interaction")
agent_interview_choice_2_part_2 = read_from_file("agent_interview_prompt_choice_2_part_2", "Prompt/choice_2_prompts_no_interaction")

# Choice 3
agent_interview_choice_3_part_1 = read_from_file("agent_interview_prompt_choice_3_part_1", "Prompt/choice_3_prompts_share")
agent_interview_choice_3_part_2 = read_from_file("agent_interview_prompt_choice_3_part_2", "Prompt/choice_3_prompts_share")
agent_interview_choice_3_part_3 = read_from_file("agent_interview_prompt_choice_3_part_3", "Prompt/choice_3_prompts_share")

# Choice 4
agent_interview_choice_4_part_1 = read_from_file("agent_interview_prompt_choice_4_part_1", "Prompt/choice_4_prompts_like")
agent_interview_choice_4_part_2 = read_from_file("agent_interview_prompt_choice_4_part_2", "Prompt/choice_4_prompts_like")
agent_interview_choice_4_part_3 = read_from_file("agent_interview_prompt_choice_4_part_3", "Prompt/choice_4_prompts_like")

# Choice 5
agent_interview_choice_5_part_1 = read_from_file("agent_interview_prompt_choice_5_part_1", "Prompt/choice_5_prompts_dislike")
agent_interview_choice_5_part_2 = read_from_file("agent_interview_prompt_choice_5_part_2", "Prompt/choice_5_prompts_dislike")
agent_interview_choice_5_part_3 = read_from_file("agent_interview_prompt_choice_5_part_3", "Prompt/choice_5_prompts_dislike")

# Choice 6
agent_interview_choice_6_part_1 = read_from_file("agent_interview_prompt_choice_6_part_1", "Prompt/choice_6_prompts_comment")
agent_interview_choice_6_part_2 = read_from_file("agent_interview_prompt_choice_6_part_2", "Prompt/choice_6_prompts_comment")
agent_interview_choice_6_part_3 = read_from_file("agent_interview_prompt_choice_6_part_3", "Prompt/choice_6_prompts_comment")


# --------- #

# AGENT BEHAVIOR #
agent_behavior_introduction = read_from_file("behavior_introduction_prompt", "Prompt")

# --------- #

def get_activity_summary_prompt(agent_name: str, current_iteration: int, never_threshold: int = 0) -> str:
    activity_labels = [
        "Published new content",
        "Not interacted with the social network",
        "Shared content published by another user",
        "Liked, disliked, or commented on content published by another user"
    ]

    activity = get_activity(agent_name)
    if activity is None:
        return read_from_file("no_activity_data", "Prompt/activity_memory_prompts")

    prompt_parts = []

    # 1. Last performed action
    if 0 in activity:
        last_action_index = activity.index(0)
        template = read_from_file("last_action", "Prompt/activity_memory_prompts")
        prompt_parts.append(template.format(activity_labels[last_action_index]))

    # 2. Never performed actions (only if current_iteration >= threshold)
    never_indices = []
    if current_iteration >= never_threshold:
        never_indices = [i for i, count in enumerate(activity) if count == current_iteration]
        if never_indices:
            if len(never_indices) == 1:
                template = read_from_file("never_singular", "Prompt/activity_memory_prompts")
                prompt_parts.append(template.format(activity_labels[never_indices[0]]))
            else:
                actions = ", ".join([activity_labels[i] for i in never_indices])
                template = read_from_file("never_plural", "Prompt/activity_memory_prompts")
                prompt_parts.append(template.format(actions))

    # 3. Inactive actions
    other_indices = [
        i for i in range(4)
        if i != activity.index(0) and i not in never_indices
    ]

    count_groups = {}
    for i in other_indices:
        count = activity[i]
        if count not in count_groups:
            count_groups[count] = []
        count_groups[count].append(activity_labels[i])

    for count, labels in count_groups.items():
        if len(labels) == 1:
            template = read_from_file("inactive_singular", "Prompt/activity_memory_prompts")
            prompt_parts.append(template.format(count, labels[0]))
        else:
            joined_labels = ", ".join(labels)
            template = read_from_file("inactive_plural", "Prompt/activity_memory_prompts")
            prompt_parts.append(template.format(count, joined_labels))

    introduction = read_from_file("activity_mem_intro_prompt", "Prompt/activity_memory_prompts")

    return "\n\n" + introduction + "\n" + "\n".join(prompt_parts)








# # AGENT ACTIVITY SUMMARY #
# def get_activity_summary_prompt(agent_name: str, current_iteration: int) -> str:
#     """
#     Returns a natural language summary of the agent's recent activity based on short-term activity memory.
#     """
#     activity_labels = [
#         "Published new content",
#         "Not interacted with the social network",
#         "Shared content published by another user",
#         "Liked, disliked, or commented on content published by another user"
#     ]

#     activity = get_activity(agent_name)
#     if activity is None:
#         return "No activity data available."

#     prompt_parts = []

#     # 1. Last performed action
#     if 0 in activity:
#         last_action_index = activity.index(0)
#         last_action_str = f"Your last action was: {activity_labels[last_action_index]}."
#         prompt_parts.append(last_action_str)

#     # 2. Actions never performed (counter == current_iteration)
#     never_performed_indices = [i for i, count in enumerate(activity) if count == current_iteration]
#     if never_performed_indices:
#         if len(never_performed_indices) == 1:
#             label = activity_labels[never_performed_indices[0]]
#             never_str = f"You have never performed the following action: {label}."
#         else:
#             labels = ", ".join([activity_labels[i] for i in never_performed_indices])
#             never_str = f"You have never performed the following actions: {labels}."
#         prompt_parts.append(never_str)

#     # 3. Other actions and how long ago they were performed
#     other_indices = [
#         i for i in range(4)
#         if i != activity.index(0) and i not in never_performed_indices
#     ]

#     # Group actions by same inactivity count
#     count_groups = {}
#     for i in other_indices:
#         count = activity[i]
#         if count not in count_groups:
#             count_groups[count] = []
#         count_groups[count].append(activity_labels[i])

#     for count, labels in count_groups.items():
#         if len(labels) == 1:
#             prompt_parts.append(
#                 f"You haven't performed the following action for {count} iterations: {labels[0]}."
#             )
#         else:
#             joined_labels = ", ".join(labels)
#             prompt_parts.append(
#                 f"You haven't performed the following actions for {count} iterations: {joined_labels}."
#             )

#     return "\n".join(prompt_parts)