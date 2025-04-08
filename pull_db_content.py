from ollama import embed
from database_connect_embeddings import get_psql_session, TextEmbedding

query = "Tell me about human rights in Germany."
query_embedding = embed(model="deepseek-r1:8b", input=query)["embeddings"][0]

def search_embeddings(query_embedding, limit=5):

    # similarity_threshold = .7
    query = session.query(TextEmbedding.sentence_number, TextEmbedding.content, TextEmbedding.file_name, 
                          TextEmbedding.embedding.cosine_distance(query_embedding).label("distance"))\
                .order_by("distance").limit(limit).all()
                #.filter(TextEmbedding.embedding.cosine_distance(query_embedding) < similarity_threshold)\
    return(query)

session = get_psql_session()
query_result = search_embeddings(query_embedding=query_embedding, limit=5)