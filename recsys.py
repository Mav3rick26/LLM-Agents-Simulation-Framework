from short_term_memory import short_term_memory
from long_term_memory import long_term_memory


def search_recommended_contents(query: str, friends_list):
    friends_name_list = []
    for friend in friends_list:
        friends_name_list.append(str(friend.name.lower()))

    try:
        res_stm = short_term_memory.query(
            query_texts=query,
            n_results=max(10, short_term_memory.count()),
            where={
                "Author": {
                    "$in": friends_name_list
                }
            },
            include=["metadatas", "documents", "distances", "embeddings"],
        )

        res_ltm = long_term_memory.query(
            query_texts=query,
            n_results=max(10, long_term_memory.count()),
            where={
                "Author": {
                    "$in": friends_name_list
                }
            },
            include=["metadatas", "documents", "distances", "embeddings"],
        )

        # Funzione per verificare se ci sono elementi in una lista
        def has_elements(result):
            return any(result.get('distances', [[]])[0])

        def initialize_dict(d):
            for key in ['ids', 'distances', 'metadatas', 'documents', 'uris', 'data']:
                if d.get(key) is None:
                    d[key] = [[]]
            return d

        res_stm = initialize_dict(res_stm)
        res_ltm = initialize_dict(res_ltm)

        # Verifica se ci sono elementi nella lista annidata sotto 'distances' in res_ltm
        for key in ['ids', 'distances', 'metadatas', 'documents']:
            if res_stm.get(key) is None:
                res_stm[key] = [[]]
            if res_ltm.get(key) is None:
                res_ltm[key] = [[]]

        # Verifica se ci sono elementi nella lista annidata sotto 'ids' in res_ltm
        if has_elements(res_ltm):
            # Unisci i risultati dei due dizionari, concatenando correttamente le liste interne
            combined_res = {
                key: [res_stm[key][0] + res_ltm[key][0]] for key in set(res_stm) | set(res_ltm)
            }
        else:
            combined_res = res_stm

        # Unisci le liste interne in una lista di tuple
        combined_tuples = list(zip(
            combined_res['ids'][0],
            combined_res['distances'][0],
            combined_res['metadatas'][0],
            combined_res['embeddings'][0],
            combined_res['documents'][0],
        ))

        # Ordina la lista di tuple in base al primo elemento (distances) in ordine decrescente
        combined_sorted = sorted(combined_tuples, key=lambda x: x[1], reverse=True)

        # Decomprimi la lista di tuple in liste separate
        combined_res['ids'][0], combined_res['distances'][0], combined_res['metadatas'][0], combined_res['embeddings'][0], combined_res['documents'][0] = map(list, zip(*combined_sorted))
        return combined_res
    except Exception as e:
        print("Vector search failed: ", e)

