from ollama import embed
from database_connect_embeddings import get_psql_session, TextEmbedding

query = "Tell me about human rights in Germany."
query_embedding = embed(model="custom_deepseek", input=query)["embeddings"][0]

# Finding the content from our database which is most similar to the query
def search_embeddings(query_embedding, session, limit=5):
    return session.query(TextEmbedding.id, TextEmbedding.sentence_number, TextEmbedding.content, TextEmbedding.file_name, 
        TextEmbedding.embedding.cosine_distance(query_embedding).label("distance") )\
        .order_by("distance").limit(limit).all()

session = get_psql_session()
query_result = search_embeddings(query_embedding=query_embedding, session=session, limit=5)

# Extracting sentences with a fixed window before and after our target sentence.

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

# get_surrounding_sentences(8222, 'Human_rights_in_Gabon.txt', 5)
