import sys
from ollama import embed
from database_connect_embeddings import get_psql_session, TextEmbedding
from pull_db_content import search_embeddings, get_surrounding_sentences

# Identify how many search results till we have 5 matches that generate non-overlapping windows.
def is_unique_to_window(existing_matches, current_match):
    
    for match in existing_matches:
        if match[3] != current_match[3]:
            continue
        if match[1] > current_match[1] + 5 or match[1] < current_match[1] - 5:
            continue
        else:
            return False
    
    return True

# Getting unique matches from search results
def get_filtered_matches(search_results):
    unique_count = 0
    matches = []
    for result in search_results:

        if unique_count >= 5:
            break;
        if is_unique_to_window(matches, result):
            unique_count += 1
            
        matches.append(result)

    return matches


def search_by_query(query, num_matches=5, window_size=5):

    session = get_psql_session()
    query_embedding = embed(model="custom_deepseek", input=query)["embeddings"][0]
    search_results = search_embeddings(query_embedding, session=session, limit=num_matches * (2*window_size + 1) )
    filtered_matches = get_filtered_matches(search_results)

    entry_ids = [i[0] for i in filtered_matches]
    file_names = [i[3] for i in filtered_matches]

    return get_surrounding_sentences(entry_ids=entry_ids, file_names=file_names, group_window_size=window_size, session=session)


if __name__=="__main__":

    query = "Tell me about children's rights in Germany."

    # filtered_matches = get_filtered_matches(search_results)
    
    if len(sys.argv) > 1:
        # raise ValueError("Please pass a query when calling the script.")
        query = sys.argv[1]

    context = search_by_query(query)

    for i in context:
        print(i, "\n")
