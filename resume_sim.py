import pandas as pd
from short_term_memory import short_term_memory
from long_term_memory import long_term_memory


def get_iteration():
    try:
        res = short_term_memory.get(
            where={
                "Iteration": {
                    "$gte": 0
                }
            },
            include=["metadatas"],
        )
        iterations = [metadata['Iteration'] for metadata in res['metadatas']]
        if not iterations:
            max_iteration = 0
        else:
            max_iteration = max(iterations)
        return max_iteration
    except Exception as e:
        print("Vector search failed : ", e)


def load_actions_dict(csv_file_path):
    actions_dict = []
    df = pd.read_csv(csv_file_path)
    for index, row in df.iterrows():
        actions_dict.append({
            'Iteration': row['Iteration'],
            'Agent': row['Agent'],
            'Choice': row['Choice'],
            'Reason': row['Reason'],
            'Content': row['Content']
        })
    return actions_dict


def load_comments_dict(csv_file_path):
    comments_dict = []
    df = pd.read_csv(csv_file_path)
    for index, row in df.iterrows():
        comments_dict.append({
            'Iteration': row['Iteration'],
            'Commenting Agent': row['Commenting Agent'],
            'Source Agent': row['Source Agent'],
            'Content': row['Content'],
            'Comment History': row['Comment History'],
            'Number of Comments': int(row['Number of Comments'])
        })
    return comments_dict


def load_connections_dict(csv_file_path):
    connections_dict = []
    df = pd.read_csv(csv_file_path)
    for index, row in df.iterrows():
        connections_dict.append({
            'Iteration': row['Iteration'],
            'Agent': row['Agent'],
            'Followed Agent': row['Followed Agent'],
        })
    return connections_dict


def load_interviews_dict(csv_file_path):
    interviews_dict = []
    df = pd.read_csv(csv_file_path)
    for index, row in df.iterrows():
        interviews_dict.append({
            'Iteration': row['Iteration'],
            'Agent': row['Agent'],
            'Main Influence': row['Main Influence'],
            'Explanation': row['Explanation']
        })
    return interviews_dict


def load_stm(csv_file_path):
    df = pd.read_csv(csv_file_path)
    ids: list = []
    metadatas: list = []
    documents: list = []
    for index, row in df.iterrows():
        ids.append(row['ID'])
        metadatas.append({"Author": row['Author'], "Virality Score": row['Virality Score'], "Sentiment Score": row['Sentiment Score'], "Iteration": row['Iteration']})
        documents.append(row['Document'])

    try:
        short_term_memory.add(
            ids=ids,
            metadatas=metadatas,
            documents=documents
        )
    except Exception as e:
        print("Add data to db failed: ", e)


def load_ltm(csv_file_path):
    df = pd.read_csv(csv_file_path)
    ids: list = []
    metadatas: list = []
    documents: list = []
    for index, row in df.iterrows():
        ids.append(row['ID'])
        metadatas.append({"Author": row['Author'], "Virality Score": row['Virality Score'], "Sentiment Score": row['Sentiment Score'], "Iteration": row['Iteration']})
        documents.append(row['Document'])

    try:
        long_term_memory.add(
            ids=ids,
            metadatas=metadatas,
            documents=documents
        )
    except Exception as e:
        print("Add data to db failed: ", e)
