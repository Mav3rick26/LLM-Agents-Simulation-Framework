import chromadb
from utils import np
from chromadb.utils import embedding_functions
from long_term_memory import add_content_to_ltm

embedding_function = embedding_functions.DefaultEmbeddingFunction()
client = chromadb.PersistentClient(path="_memories/short_term_memory")
short_term_memory = client.get_or_create_collection(name="short_term_memory", embedding_function=embedding_function, metadata={"hnsw:space": "cosine"})


def get_stm():  # Only get documents and ids from short term memory
    res = short_term_memory.get(
        include=["documents", "metadatas"]
    )
    return res


# def add_content_to_stm(agent, content, virality_score, sentiment_score, iteration):
#     ids: list = []
#     metadatas: list = []
#     documents: list = []

#     ids.append(str(agent.name.lower()) + "_" + str(iteration + 1))
#     metadatas.append({"Author": str(agent.name.lower()), "Virality Score": virality_score, "Sentiment Score": sentiment_score, "Iteration": iteration + 1})
#     documents.append(content)

#     try:
#         short_term_memory.add(
#             ids=ids,
#             metadatas=metadatas,
#             documents=documents
#         )
#     except Exception as e:
#         print("Add data to db failed: ", e)


# def add_content_to_stm(agent, content, virality_score, sentiment_score, iteration, is_retweet=False):
#     ids: list = []
#     metadatas: list = []
#     documents: list = []

#     content_id = str(agent.name.lower()) + "_" + str(iteration + 1)

#     ids.append(content_id)
#     metadatas.append({
#         "Author": str(agent.name.lower()),
#         "Virality Score": virality_score,
#         "Sentiment Score": sentiment_score,
#         "Iteration": iteration + 1,
#         "Content_ID": content_id,
#         "Is_Retweet": is_retweet
#     })
#     documents.append(content)

#     try:
#         short_term_memory.add(
#             ids=ids,
#             metadatas=metadatas,
#             documents=documents
#         )
#     except Exception as e:
#         print("Add data to STM failed: ", e)

# def add_content_to_stm(agent, content, virality_score, sentiment_score, iteration,
#                        is_retweet=False, original_content_id=None, Direct_Interaction_ID=None):
#     ids: list = []
#     metadatas: list = []
#     documents: list = []

#     content_id = str(agent.name.lower()) + "_" + str(iteration + 1)
#     ids.append(content_id)

#     metadata = {
#         "Author": str(agent.name.lower()),
#         "Virality Score": virality_score,
#         "Sentiment Score": sentiment_score,
#         "Iteration": iteration + 1
#     }

#     if is_retweet:
#         metadata["Is_Retweet"] = True
#         metadata["Original_Content_ID"] = original_content_id
#         metadata["Direct_Interaction_ID"] = Direct_Interaction_ID
#     else:
#         metadata["Is_Retweet"] = False
#         metadata["Original_Content_ID"] = content_id
#         metadata["Direct_Interaction_ID"] = content_id

#     metadatas.append(metadata)
#     documents.append(content)

#     try:
#         short_term_memory.add(
#             ids=ids,
#             metadatas=metadatas,
#             documents=documents
#         )
#     except Exception as e:
#         print("Add data to STM failed: ", e)

#     return content_id  # utile se vuoi salvarlo nell'actions_dict


def add_content_to_stm(agent, content, virality_score, sentiment_score, iteration,
                       is_retweet=False, original_content_id=None, direct_interaction_id=None):
    ids: list = []
    metadatas: list = []
    documents: list = []

    content_id = str(agent.name.lower()) + "_" + str(iteration + 1)
    ids.append(content_id)

    metadata = {
        "Author": str(agent.name.lower()),
        "Virality Score": virality_score,
        "Sentiment Score": sentiment_score,
        "Iteration": iteration + 1
    }

    if is_retweet:
        metadata["Is_Retweet"] = True
    else:
        metadata["Is_Retweet"] = False

    metadata["Original_Content_ID"] = original_content_id if original_content_id else content_id
    metadata["Direct_Interaction_ID"] = direct_interaction_id if direct_interaction_id else content_id

    metadatas.append(metadata)
    documents.append(content)

    try:
        short_term_memory.add(
            ids=ids,
            metadatas=metadatas,
            documents=documents
        )
    except Exception as e:
        print("Add data to STM failed: ", e)

    return content_id

def modify_stm_virality_score(content_id, new_virality_score):
    res = short_term_memory.get(
        ids=content_id,
        include=["metadatas"],
    )

    virality_score = res["metadatas"][0]["Virality Score"]

    short_term_memory.update(
        ids=content_id,
        metadatas=[{"Virality Score": virality_score + new_virality_score}]
    )


def modify_stm_sentiment_score(content_id, new_sentiment_score):
    res = short_term_memory.get(
        ids=content_id,
        include=["metadatas"],
    )

    current_sentiment_score = res["metadatas"][0]["Sentiment Score"]

    short_term_memory.update(
        ids=content_id,
        metadatas=[{"Sentiment Score": current_sentiment_score + new_sentiment_score}]
    )


# def evaluate_stm_content_for_ltm_transfer(content_id):
#     res = short_term_memory.get(
#         ids=content_id,
#         include=["metadatas", "documents"],
#     )

#     content_author = res["metadatas"][0]["Author"]
#     content_iteration = res["metadatas"][0]["Iteration"]
#     virality_score = res["metadatas"][0]["Virality Score"]
#     sentiment_score = res["metadatas"][0]["Sentiment Score"]

#     if virality_score >= 2 or abs(sentiment_score) >= 1:
#         add_content_to_ltm(content_id, res["documents"][0], content_author, content_iteration, virality_score, sentiment_score)
#         delete_content_from_stm(content_id)

def evaluate_stm_content_for_ltm_transfer(content_id):
    res = short_term_memory.get(
        ids=content_id,
        include=["metadatas", "documents"],
    )

    metadata = res["metadatas"][0]
    document = res["documents"][0]

    content_author = metadata.get("Author", "")
    content_iteration = metadata.get("Iteration", -1)
    virality_score = metadata.get("Virality Score", 0)
    sentiment_score = metadata.get("Sentiment Score", 0)

    original_id = metadata.get("Original_Content_ID", content_id)
    direct_id = metadata.get("Direct_Interaction_ID", content_id)

    if virality_score >= 2 or abs(sentiment_score) >= 1:
        add_content_to_ltm(
            content_id=content_id,
            content=document,
            author=content_author,
            iteration=content_iteration,
            virality_score=virality_score,
            sentiment_score=sentiment_score,
            original_content_id=original_id,
            direct_interaction_id=direct_id
        )
        delete_content_from_stm(content_id)


def delete_content_from_stm(content_id):
    short_term_memory.delete(
        ids=content_id
    )


def is_content_in_stm(content_id):
    res = short_term_memory.get(
        ids=content_id,
        include=["documents"],
    )
    return bool(res["documents"])


def get_feedbacks_from_stm(agent):
    res = short_term_memory.get(
        where={"Author": str(agent.name.lower())},
        include=["documents", "metadatas"],
    )

    num_documents = len(res['documents'])

    output_strings = []

    for i in range(num_documents):
        document = res['documents'][i]
        virality_score = res['metadatas'][i]['Virality Score']
        content_score = res['metadatas'][i]['Sentiment Score']
        output_string = f"{document} - Virality Score: {virality_score} - Content Score: {content_score}"
        output_strings.append(output_string)
    final_output = "\n".join(output_strings)
    return final_output


def get_source_agent_from_stm(content_id):
    res = short_term_memory.get(
        ids=content_id,
        include=["documents", "metadatas"],
    )

    return res["metadatas"][0]["Author"]


def calculate_recency(current_iteration, content_iteration):
    """
    Calculate the normalized recency score.
    """
    iterations_passed = current_iteration - content_iteration
    recency_score = 1.0 - iterations_passed / (iterations_passed + 1)
    return recency_score


def calculate_importance(virality_score, sentiment_score, virality_weight=0.6, sentiment_weight=0.4):
    """
    Calculate the combined importance score using a weighted average.
    """
    importance_score = (virality_score * virality_weight + abs(sentiment_score) * sentiment_weight) / (virality_weight + sentiment_weight)
    return importance_score


def decay_probability(s_i, r_i, delta, beta):
    """
    Calculate the forgetting probability for a memory M_i.

    Parameters:
    s_i (float): Normalized recency score in the range [0.0, 1.0].
    r_i (float): Normalized importance score in the range [0.0, 1.0].
    delta (float): Strength parameter in the range [0.0, 1.0].
    beta (float): Hyper-parameter controlling the power function shape.

    Returns:
    float: Forgetting probability in the range [0.0, 1.0].
    """
    power_function = max(r_i**beta, delta)
    average_score = (s_i + r_i) / 2
    forgetting_probability = 1 - average_score * power_function
    forgetting_probability = np.clip(forgetting_probability, 0.0, 1.0)
    return forgetting_probability


def content_score_decadency_law_stm(current_iteration):
    current_iteration = current_iteration + 1

    res = short_term_memory.get(
        include=["documents", "metadatas"]
    )

    delta = 1  # Decay rate
    beta = 4.0  # Importance of recency

    for i in range(len(res["documents"])):  # For each content in STM
        content_iteration = res["metadatas"][i]["Iteration"]

        virality_score = res["metadatas"][i]["Virality Score"]  # Assuming virality score is stored in metadata
        sentiment_score = res["metadatas"][i]["Sentiment Score"]  # Assuming sentiment score is stored in metadata

        # Calculate recency score
        recency_score = calculate_recency(current_iteration, content_iteration)

        # Calculate importance score
        importance_score = calculate_importance(virality_score, sentiment_score)

        # Calculate forgetting probability
        forgetting_probability = decay_probability(recency_score, importance_score, delta, beta)

        if forgetting_probability >= 0.9:
            delete_content_from_stm(res["ids"][i])


def clear_stm():
    short_term_memory.delete(
        where={"Iteration": {"$gte": 0}}
    )
