import os
from ollama import embed
from nltk.tokenize import sent_tokenize
from database_connect_embeddings import get_psql_session

import nltk
nltk.download("punkt")
nltk.download("punkt_tab")

def populate_vector_database(folder_path='all_articles'):

    session = get_psql_session()

    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)

        print("Trying: {}".format(file_path))
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            sentences = sent_tokenize(content)
            embeddings = embed(model="deepseek-r1:8b", input=sentences)["embeddings"]
            
            for i, (embedding, content) in enumerate(zip(embeddings, sentences)):
                new_embedding = TextEmbedding(embedding=embedding, content=content, file_name=filename, sentence_number=i+1)
                session.add(new_embedding)
            session.commit()

        except Exception as e:
            print(f"Error processing {filename}: {str(e)}")
            continue

    return

populate_vector_database()