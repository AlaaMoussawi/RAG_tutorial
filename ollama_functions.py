from ollama import embed, chat


embeddings = embed(model="deepseek-r1:8b", input=["Here is an example sentence I will be embedding!", "Here's a second one!"])

len(embeddings['embeddings'])


response = chat(model='deepseek-r1:8b', messages=[
  {
    'role': 'user',
    'content': 'Why is the sky blue?',
  },
])

print(response.message.content)