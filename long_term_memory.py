import chromadb
from chromadb.utils import embedding_functions

embedding_function = embedding_functions.DefaultEmbeddingFunction()
client = chromadb.PersistentClient(path="_memories/long_term_memory")
long_term_memory = client.get_or_create_collection(name="long_term_memory", embedding_function=embedding_function, metadata={"hnsw:space": "cosine"})


def get_ltm():  # Only get documents and ids from long term memory
    res = long_term_memory.get(
        include=["documents", "metadatas"]
    )
    return res


def add_content_to_ltm(content_id, content, author, iteration, virality_score, sentiment_score):
    ids: list = []
    metadatas: list = []
    documents: list = []

    ids.append(content_id)
    metadatas.append({"Author": author, "Iteration": iteration, "Virality Score": virality_score, "Sentiment Score": sentiment_score})
    documents.append(content)

    try:
        long_term_memory.add(
            ids=ids,
            metadatas=metadatas,
            documents=documents
        )
    except Exception as e:
        print("Add data to db failed: ", e)


def is_content_in_ltm(content_id):
    res = long_term_memory.get(
        ids=content_id,
        include=["documents"],
    )
    return bool(res["documents"])


def modify_ltm_virality_score(content_id, new_virality_score):
    res = long_term_memory.get(
        ids=content_id,
        include=["metadatas"],
    )

    virality_score = res["metadatas"][0]["Virality Score"]

    long_term_memory.update(
        ids=content_id,
        metadatas=[{"Virality Score": virality_score + new_virality_score}]
    )


def modify_ltm_sentiment_score(content_id, new_sentiment_score):
    res = long_term_memory.get(
        ids=content_id,
        include=["metadatas"],
    )

    current_sentiment_score = res["metadatas"][0]["Sentiment Score"]

    long_term_memory.update(
        ids=content_id,
        metadatas=[{"Sentiment Score": current_sentiment_score + new_sentiment_score}]
    )


def get_source_agent_from_ltm(content_id):
    res = long_term_memory.get(
        ids=content_id,
        include=["documents", "metadatas"],
    )

    return res["metadatas"][0]["Author"]


def get_feedbacks_from_ltm(agent):
    res = long_term_memory.get(
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


def clear_ltm():
    long_term_memory.delete(
        where={"Iteration": {"$gte": 0}}
    )
