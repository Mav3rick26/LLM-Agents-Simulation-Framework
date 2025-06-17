import pandas as pd


def save_to_csv(data, filename):
    """Converts a list of dictionaries into a DataFrame and saves it to a CSV file."""
    pd.DataFrame(data).to_csv(f'Output/{filename}.csv', index=False)


# def get_memory_data(memory):
#     """Extracts relevant data from memory for CSV conversion."""
#     return [{
#         'ID': ids,
#         'Author': metadata['Author'],
#         'Iteration': metadata['Iteration'],
#         'Sentiment Score': metadata['Sentiment Score'],
#         'Virality Score': metadata['Virality Score'],
#         'Content_ID': metadata.get('Content_ID', 'N/A'),
#         'Is_Retweet': metadata.get('Is_Retweet', False),
#         'Document': document
#     } for ids, metadata, document in zip(memory['ids'], memory['metadatas'], memory['documents'])]


def get_memory_data(memory):
    """Extracts relevant data from memory for CSV conversion."""
    return [{
        'ID': ids,
        'Author': metadata['Author'],
        'Iteration': metadata['Iteration'],
        'Sentiment Score': metadata['Sentiment Score'],
        'Virality Score': metadata['Virality Score'],
        'Content_ID': ids,
        'Is_Retweet': metadata.get('Is_Retweet', False),
        'Original_Content_ID': metadata.get('Original_Content_ID'),
        'Direct_Interaction_ID': metadata.get('Direct_Interaction_ID'),
        'Document': document
    } for ids, metadata, document in zip(memory['ids'], memory['metadatas'], memory['documents'])]