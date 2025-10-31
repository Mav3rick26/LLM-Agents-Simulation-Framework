from short_term_memory import short_term_memory
from long_term_memory import long_term_memory

import random


def search_random_contents(agent_name: str):
    print(f"\n[DEBUG] search_random_contents called for agent: {agent_name}")

    # --- Get all items from STM and LTM ---
    stm_data = short_term_memory.get(include=["metadatas", "documents"])
    ltm_data = long_term_memory.get(include=["metadatas", "documents"])

    # --- Collect all Original_Content_IDs already published by this agent ---
    agent_published_ids = set()
    for meta in (stm_data.get("metadatas") or []) + (ltm_data.get("metadatas") or []):
        if meta and isinstance(meta, dict):
            if meta.get("Author", "").lower() == agent_name.lower():
                original_id = meta.get("Original_Content_ID", "")
                if original_id:
                    agent_published_ids.add(str(original_id).lower().strip())

    print(f"[DEBUG] Agent's previously published Original_Content_IDs: {agent_published_ids}")

    # --- Combine STM + LTM results ---
    all_ids = (stm_data.get("ids") or []) + (ltm_data.get("ids") or [])
    all_metadatas = (stm_data.get("metadatas") or []) + (ltm_data.get("metadatas") or [])
    all_documents = (stm_data.get("documents") or []) + (ltm_data.get("documents") or [])

    # --- Filter out contents already published by the agent ---
    filtered_tuples = [
        (cid, meta, doc)
        for cid, meta, doc in zip(all_ids, all_metadatas, all_documents)
        if meta and str(meta.get("Original_Content_ID", "")).lower().strip() not in agent_published_ids
    ]

    # --- RANDOMIZE ORDER ---
    random.shuffle(filtered_tuples)

    # --- Rebuild the same structure ---
    combined_res = {
        "ids": [[t[0] for t in filtered_tuples]],
        "metadatas": [[t[1] for t in filtered_tuples]],
        "documents": [[t[2] for t in filtered_tuples]],
    }

    # --- Debug output ---
    print("\n[DEBUG] Random recommended contents (all authors):")
    for i, tup in enumerate(filtered_tuples[:10]):
        id_post = str(tup[1].get("Original_Content_ID", "")).lower().strip()
        print(f"   {i+1:02d}) RANDOM RECOMMENDATION: {id_post}")

    return combined_res


def search_recommended_contents(query: str, friends_list, agent_name: str):
    print(f"\n[DEBUG] search_recommended_contents called for agent: {agent_name}")
    friends_name_list = [str(friend.name.lower()) for friend in friends_list]
    print(f"[DEBUG] Friends to search from: {friends_name_list}")

    agent_published_ids = set()
    stm_data = short_term_memory.get(include=["metadatas"])
    ltm_data = long_term_memory.get(include=["metadatas"])

    for meta in (stm_data.get("metadatas") or []) + (ltm_data.get("metadatas") or []):   # Unisco STM e LTM per evitare duplicati
    #for meta in (stm_data.get("metadatas") or []):      # Solo STM per evitare duplicati
        if meta and isinstance(meta, dict):
            if meta.get("Author", "").lower() == agent_name.lower():
                original_id = meta.get("Original_Content_ID", "")
                if original_id:
                    agent_published_ids.add(str(original_id).lower().strip())

    print(f"[DEBUG] Agent's previously published Original_Content_IDs (normalized): {agent_published_ids}")

    where_filter = {
        "Author": {"$in": friends_name_list},
        "Original_Content_ID": {"$nin": list(agent_published_ids)}
    }

    try:
        res_stm = short_term_memory.query(
            query_texts=query,
            n_results=max(10, short_term_memory.count()),
            where = {
                "$and": [
                    {"Author": {"$in": friends_name_list}},
                    {"Original_Content_ID": {"$nin": list(agent_published_ids)}}
                ]
            },
            include=["metadatas", "documents", "distances", "embeddings"],
        )

        res_ltm = long_term_memory.query(
            query_texts=query,
            n_results=max(10, long_term_memory.count()),
            where = {
                "$and": [
                    {"Author": {"$in": friends_name_list}},
                    {"Original_Content_ID": {"$nin": list(agent_published_ids)}}
                ]
            },
            include=["metadatas", "documents", "distances", "embeddings"],
        )

        def initialize_dict(d):
            for key in ['ids', 'distances', 'metadatas', 'documents', 'embeddings']:
                if d.get(key) is None or d.get(key) == [None]:
                    d[key] = [[]]
            return d

        def has_elements(result):
            return any(result.get('distances', [[]])[0])

        res_stm = initialize_dict(res_stm)
        res_ltm = initialize_dict(res_ltm)

        if has_elements(res_ltm):
            combined_res = {}
            for key in set(res_stm) | set(res_ltm):
                list_stm = res_stm.get(key, [[]])
                list_ltm = res_ltm.get(key, [[]])
                val_stm = list_stm[0] if list_stm and isinstance(list_stm[0], list) else []
                val_ltm = list_ltm[0] if list_ltm and isinstance(list_ltm[0], list) else []
                combined_res[key] = [val_stm + val_ltm]
        else:
            combined_res = res_stm

        combined_tuples = list(zip(
            combined_res['ids'][0],
            combined_res['distances'][0],
            combined_res['metadatas'][0],
            combined_res['embeddings'][0],
            combined_res['documents'][0],
        ))

        filtered_tuples = combined_tuples

        # DEBUG: contenuti finali
        print("\n[DEBUG] Contenuti raccomandati dopo il filtro automatico (da where):")
        for i, tup in enumerate(filtered_tuples):
            id_post = str(tup[2].get("Original_Content_ID", "")).lower().strip()
            print(f"   {i+1:02d}) FINAL RECOMMENDATION: {id_post}")

        # Ordinamento per distanza (similarità)
        combined_sorted = sorted(filtered_tuples, key=lambda x: x[1], reverse=True)

        # Ricostruzione della struttura finale
        if combined_sorted:
            combined_res['ids'][0], combined_res['distances'][0], combined_res['metadatas'][0], combined_res['embeddings'][0], combined_res['documents'][0] = map(list, zip(*combined_sorted))
        else:
            combined_res['ids'][0] = []
            combined_res['distances'][0] = []
            combined_res['metadatas'][0] = []
            combined_res['embeddings'][0] = []
            combined_res['documents'][0] = []

        return combined_res

    except Exception as e:
        print("Vector search failed: ", e)
