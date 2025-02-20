import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from utils import get_embedding, calculate_similarity, model


def compute_simulation_saturation(num_iterations):
    file_path = 'Output/simulation_log.csv'
    df = pd.read_csv(file_path)

    filtered_df = df[df['Choice'] == "Posting new content"]

    seen_contents = set()  # Track the contents already published
    repeated_counts = []  # Count the repeated contents for each iteration
    num_repeated = 0  # Number of repeated contents

    for iteration in range(1, num_iterations + 1):
        group = filtered_df[filtered_df['Iteration'] == iteration]  # Filter the data for the current iteration

        for row in group.itertuples():  # Iterate over the rows of the filtered data
            if pd.notna(row.Content):  # Check if the 'Content' column is not empty
                embedding = get_embedding(row.Content)  # Get the embedding for the content
                embedding_tuple = tuple(embedding.tolist())  # Convert the NumPy array to a tuple
                is_in_seen_contents = False
                if iteration == 1:
                    seen_contents.add(embedding_tuple)
                else:
                    for seen_content in seen_contents:
                        if calculate_similarity(embedding, np.array(seen_content)) > 0.8:
                            is_in_seen_contents = True
                            num_repeated += 1
                            break

                    if not is_in_seen_contents:
                        seen_contents.add(embedding_tuple)

        repeated_counts.append(num_repeated)
        print(f"Iteration {iteration}: {num_repeated} repeated contents")

    # Plot the repeated contents for each iteration
    plt.plot(range(1, len(repeated_counts) + 1), repeated_counts, marker='o')
    plt.title('Number of repeated contents for iteration')
    plt.xlabel('Iteration')
    plt.xticks(range(1, len(repeated_counts) + 1))
    plt.ylabel('Repeated Contents')
    plt.grid(True)
    plt.show()


def compute_simulation_saturation_OLD():
    file_path = 'Output/simulation_log.csv'
    data = pd.read_csv(file_path)

    data['Text'] = data['Reason'].fillna('') + ' ' + data['Content'].fillna('')  # Concatenate the 'Reason' and 'Content' texts for each iteration
    grouped_data = data.groupby('Iteration')['Text'].apply(lambda x: ' '.join(x)).reset_index()  # Group the data by 'Iteration' and concatenate the texts within each group

    model = SentenceTransformer('all-MiniLM-L6-v2')
    embeddings = model.encode(grouped_data['Text'].tolist())

    # Calculate cosine similarity between each iteration and all previous iterations
    similarities = []
    for i in range(1, len(embeddings)):
        sim = cosine_similarity([embeddings[i]], embeddings[:i])
        similarities.append(sim.max())  # Take the maximum similarity with previous iterations

    # Plot the similarities
    iterations = list(range(2, len(similarities) + 2))  # Generate a list of iteration numbers for the x-axis (starting from 2)
    plt.plot(iterations, similarities, marker='o', label='Cosine Similarity')
    plt.axhline(y=0.95, color='r', linestyle='--', label='Saturation Threshold')
    plt.xlabel('Iterations')
    plt.ylabel('Cosine Similarity')
    plt.title('Similarity between Iterations and Previous Ones')
    plt.legend()
    plt.grid(True)
    plt.show()

    # Check if the last N iterations have a similarity greater than 0.95
    N = 5
    saturation = all(s > 0.95 for s in similarities[-N:])
    print("Is the simulation saturating:", saturation)
