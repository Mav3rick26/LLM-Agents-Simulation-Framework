from short_term_memory import short_term_memory
from long_term_memory import long_term_memory

# def search_recommended_contents(query: str, friends_list, agent_name: str):
#     print(f"\n[DEBUG] search_recommended_contents called for agent: {agent_name}")
#     friends_name_list = [str(friend.name.lower()) for friend in friends_list]
#     print(f"[DEBUG] Friends to search from: {friends_name_list}")
#     try:
#         res_stm = short_term_memory.query(
#             query_texts=query,
#             n_results=max(10, short_term_memory.count()),
#             where={"Author": {"$in": friends_name_list}},
#             include=["metadatas", "documents", "distances", "embeddings"],
#         )

#         print("[DEBUG] Query STM executed.")
#         if res_stm is None:
#             print("[ERROR] res_stm is None!")
#         else:
#             print(f"[DEBUG] STM Results - IDs: {res_stm.get('ids', [[]])[0]}")

#         res_ltm = long_term_memory.query(
#             query_texts=query,
#             n_results=max(10, long_term_memory.count()),
#             where={"Author": {"$in": friends_name_list}},
#             include=["metadatas", "documents", "distances", "embeddings"],
#         )

#         print("[DEBUG] Query LTM executed.")
#         if res_ltm is None:
#             print("[ERROR] res_ltm is None!")
#         else:
#             print(f"[DEBUG] LTM Results - IDs: {res_ltm.get('ids', [[]])[0]}")

#         def has_elements(result):
#             return any(result.get('distances', [[]])[0])

#         # def initialize_dict(d):
#         #     for key in ['ids', 'distances', 'metadatas', 'documents', 'embeddings']:
#         #         if d.get(key) is None:
#         #             d[key] = [[]]
#         #     return d
        
#         def initialize_dict(d):
#             for key in ['ids', 'distances', 'metadatas', 'documents', 'embeddings']:
#                 if d.get(key) is None or d.get(key) == [None]:
#                     print(f"[DEBUG] Key '{key}' was missing or None. Initializing to [[]].")
#                     d[key] = [[]]
#             return d

#         res_stm = initialize_dict(res_stm)
#         res_ltm = initialize_dict(res_ltm)
#         print(f"[DEBUG] After initialization: STM -> {res_stm['ids'][0]}, LTM -> {res_ltm['ids'][0]}")

#         # if has_elements(res_ltm):
#         #     combined_res = {
#         #         key: [res_stm[key][0] + res_ltm[key][0]] for key in set(res_stm) | set(res_ltm)
#         #     }
#         # else:
#         #     combined_res = res_stm

#         if has_elements(res_ltm):
#             combined_res = {}
#             for key in set(res_stm) | set(res_ltm):
#                 list_stm = res_stm.get(key, [[]])
#                 list_ltm = res_ltm.get(key, [[]])
#                 val_stm = list_stm[0] if list_stm and isinstance(list_stm[0], list) else []
#                 val_ltm = list_ltm[0] if list_ltm and isinstance(list_ltm[0], list) else []
#                 combined_res[key] = [val_stm + val_ltm]
#         else:
#             combined_res = res_stm

#         print("[DEBUG] Controllo contenuti prima dello zip:")
#         print(f"  IDs: {combined_res.get('ids', [[]])[0]}")
#         print(f"  Distances: {combined_res.get('distances', [[]])[0]}")
#         print(f"  Metadatas: {combined_res.get('metadatas', [[]])[0]}")
#         print(f"  Embeddings: {combined_res.get('embeddings', [[]])[0]}")
#         print(f"  Documents: {combined_res.get('documents', [[]])[0]}")

#         # Controlla anche se sono None esplicitamente
#         for key in ['ids', 'distances', 'metadatas', 'embeddings', 'documents']:
#             val = combined_res.get(key)
#             if val is None:
#                 print(f"[WARNING] combined_res['{key}'] is None!")
#             elif val == [None]:
#                 print(f"[WARNING] combined_res['{key}'] == [None]!")
#             elif val == [[]]:
#                 print(f"[WARNING] combined_res['{key}'] is an empty list.")
#             else:
#                 print(f"[DEBUG] combined_res['{key}'] seems OK.")

#         combined_tuples = list(zip(
#             combined_res['ids'][0],
#             combined_res['distances'][0],
#             combined_res['metadatas'][0],
#             combined_res['embeddings'][0],
#             combined_res['documents'][0],
#         ))

#         # FILTRO ANTI-LOOP
#         agent_name = agent_name.lower()

#         # Recupera tutti gli original content ID già pubblicati o ritwittati dall'agente stesso
#         # agent_published_ids = set()
#         # stm_data = short_term_memory.get(include=["metadatas"])
#         # for meta in stm_data["metadatas"]:
#         #     if meta.get("Author", "").lower() == agent_name:
#         #         agent_published_ids.add(meta.get("Original_Content_ID", ""))
#         agent_published_ids = set()
#         stm_data = short_term_memory.get(include=["metadatas"])
#         ltm_data = long_term_memory.get(include=["metadatas"])
#         for meta in stm_data["metadatas"] + ltm_data["metadatas"]:
#             if meta.get("Author", "").lower() == agent_name:
#                 original_id = meta.get("Original_Content_ID", "")
#                 if original_id:
#                     agent_published_ids.add(original_id)

#         # Filtro i contenuti che hanno già lo stesso Original_Content_ID
#         filtered_tuples = [
#             tup for tup in combined_tuples
#             if tup[2].get("Original_Content_ID", "") not in agent_published_ids
#         ]
#         print(f"[DEBUG] Filtering out already posted Original_Content_IDs: {agent_published_ids}")
#         print(f"[DEBUG] Before filtering - Combined tuples: {len(combined_tuples)}")
#         print(f"[DEBUG] After filtering - Filtered tuples: {len(filtered_tuples)}")
#         # Ordina e decomprimi
#         combined_sorted = sorted(filtered_tuples, key=lambda x: x[1], reverse=True)

#         if combined_sorted:
#             combined_res['ids'][0], combined_res['distances'][0], combined_res['metadatas'][0], combined_res['embeddings'][0], combined_res['documents'][0] = map(list, zip(*combined_sorted))
#         else:
#             combined_res['ids'][0] = []
#             combined_res['distances'][0] = []
#             combined_res['metadatas'][0] = []
#             combined_res['embeddings'][0] = []
#             combined_res['documents'][0] = []
        
#         if not combined_res['ids'][0]:
#             print("[DEBUG] No content passed the filtering - returning empty recommendation.")
#         return combined_res

#     except Exception as e:
#         print("Vector search failed: ", e)



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

    #     # Recupero ID contenuti già pubblicati dall’agente
    #     agent_name = agent_name.lower()

    #     # Normalizza STM e LTM: se metadatas è [None] o None, sostituisci con []
    #     stm_data = short_term_memory.get(include=["metadatas"])
    #     ltm_data = long_term_memory.get(include=["metadatas"])

    #     stm_metas = stm_data.get("metadatas", [])
    #     ltm_metas = ltm_data.get("metadatas", [])

    #     if stm_metas == [None] or stm_metas is None:
    #         stm_metas = []

    #     if ltm_metas == [None] or ltm_metas is None:
    #         ltm_metas = []

    #     agent_published_ids = set()
    #     for meta in stm_metas + ltm_metas:
    #         if not isinstance(meta, dict):
    #             continue
    #         if meta.get("Author", "").lower() == agent_name:
    #             original_id = meta.get("Original_Content_ID", "")
    #             if original_id:
    #                 agent_published_ids.add(str(original_id).lower().strip())

    #     # DEBUG: stampa contenuti già pubblicati (normalizzati)
    #     print(f"\n[DEBUG] Agent name (normalized): {agent_name}")
    #     print("[DEBUG] Agent's previously published Original_Content_IDs (normalized):")
    #     for id in agent_published_ids:
    #         print(f"   - {id}")

    #     # DEBUG: stampa contenuti proposti prima del filtro
    #     print("\n[DEBUG] Contenuti proposti (prima del filtro):")
    #     for i, tup in enumerate(combined_tuples):
    #         proposed_id = str(tup[2].get("Original_Content_ID", "")).lower().strip()
    #         passed = proposed_id not in agent_published_ids
    #         print(f"   {i+1:02d}) Proposed: {proposed_id}  --> PASSES FILTER? {passed}")
    #         if not passed:
    #             print(f"       ↪️ Motivo: già presente in STM/LTM")

    #     # Filtro i contenuti già pubblicati
    #     filtered_tuples = [
    #         tup for tup in combined_tuples
    #         if str(tup[2].get("Original_Content_ID", "")).lower().strip() not in agent_published_ids
    #     ]

    #     # DEBUG: contenuti dopo il filtro
    #     print("\n[DEBUG] Contenuti effettivamente raccomandati (dopo filtro):")
    #     for i, tup in enumerate(filtered_tuples):
    #         id_post = str(tup[2].get("Original_Content_ID", "")).lower().strip()
    #         print(f"   {i+1:02d}) FINAL RECOMMENDATION: {id_post}")
    #         if id_post in agent_published_ids:
    #             print(f"       ❌ ERRORE: questo contenuto è già stato condiviso!")

    #     # Controllo generale di sicurezza
    #     if any(str(tup[2].get("Original_Content_ID", "")).lower().strip() in agent_published_ids for tup in filtered_tuples):
    #         print("[❌ WARNING] ATTENZIONE: È passato almeno un contenuto già condiviso precedentemente!")

    #     # Ordinamento per distanza (similarità)
    #     combined_sorted = sorted(filtered_tuples, key=lambda x: x[1], reverse=True)

    #     # Ricostruzione della struttura finale
    #     if combined_sorted:
    #         combined_res['ids'][0], combined_res['distances'][0], combined_res['metadatas'][0], combined_res['embeddings'][0], combined_res['documents'][0] = map(list, zip(*combined_sorted))
    #     else:
    #         combined_res['ids'][0] = []
    #         combined_res['distances'][0] = []
    #         combined_res['metadatas'][0] = []
    #         combined_res['embeddings'][0] = []
    #         combined_res['documents'][0] = []

    #     return combined_res

    # except Exception as e:
    #     print("Vector search failed: ", e)
