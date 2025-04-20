import sys
from ollama import embed
from pull_db_content import search_embeddings, get_surrounding_sentences

query = "Tell me about human rights in Germany."

if (len(sys.argv) == 0):
    continue    
    # raise ValueError("Please pass a query when calling the script.")
else:
    query = sys.argv[1]

query_embedding = embed(model="deepseek-r1:8b", input=query)["embeddings"][0]

num_matches = 5
window_size = 5
search_results = search_embeddings(query_embedding=query_embedding, limit=num_matches * (2*window_size + 1) )

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
def get_needed_matches(search_results):

    unique_count = 0
    matches = []
    for result in search_results:

        if unique_count >= 5:
            break;
        if is_unique_to_window(matches, result):
            unique_count += 1
            
        matches.append(result)

    return matches

filtered_matches = get_needed_matches(search_results)