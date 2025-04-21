import sys
from ollama import embed
from pull_db_content import search_embeddings, get_surrounding_sentences

query = "Tell me about human rights in Germany."
if len(sys.argv) > 1:
    # raise ValueError("Please pass a query when calling the script.")
    query = sys.argv[1]

# query_embedding = embed(model="deepseek-r1:8b", input=query)["embeddings"][0]

num_matches = 5
window_size = 5
# search_results = search_embeddings(query_embedding=query_embedding, limit=num_matches * (2*window_size + 1) )

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

# filtered_matches = get_filtered_matches(search_results)
# Finding the content from our database which is most similar to the query
def search_embeddings(query_embedding, session, limit=5):
    return session.query(TextEmbedding.id, TextEmbedding.sentence_number, TextEmbedding.content, TextEmbedding.file_name, 
        TextEmbedding.embedding.cosine_distance(query_embedding).label("distance") )\
        .order_by("distance").limit(limit).all()



def get_surrounding_sentences(entry_ids, file_names, group_window_size, session):

    surrounding_sentences = []
    if isinstance(entry_ids, list) and isinstance(file_names, list):
        for entry_id, file_name in zip(entry_ids, file_names):
            surrounding_sentences.append(
                session.query(TextEmbedding.id, TextEmbedding.sentence_number, TextEmbedding.content, TextEmbedding.file_name)\
                .filter(TextEmbedding.id >= entry_id - group_window_size)\
                .filter(TextEmbedding.id <= entry_id + group_window_size)\
                .filter(TextEmbedding.file_name == file_name).all()
            )
        
        return surrounding_sentences
    
    else:
        return [session.query(TextEmbedding.id, TextEmbedding.sentence_number, TextEmbedding.content, TextEmbedding.file_name)\
            .filter(TextEmbedding.id >= entry_ids - group_window_size)\
            .filter(TextEmbedding.id <= entry_ids + group_window_size)\
            .filter(TextEmbedding.file_name == file_names).all()]


def search_by_query(query, num_matches=5, window_size=5):

    session = get_psql_session()
    query_embedding = embed(model="deepseek-r1:8b", input=query)["embeddings"][0]
    search_results = search_embeddings(query_embedding, session=session, limit=num_matches * (2*window_size + 1) )
    filtered_matches = get_filtered_matches(search_results)

    entry_ids = [i[0] for i in filtered_matches]
    file_names = [i[3] for i in filtered_matches]

    return get_surrounding_sentences(entry_ids=entry_ids, file_names=file_names, group_window_size=window_size, session=session)

context = search_by_query(query)

for i in context:
    print(len(i))