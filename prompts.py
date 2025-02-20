from utils import read_from_file

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
