from prepare_content import search_by_query
from ollama import chat
import sys

query = "Tell me about children's rights in Germany."
if len(sys.argv) > 1:
    query = sys.argv[1]

context = search_by_query(query)

prompt = f"<|content_start>{context} \
<|content_end> {query}"

response = chat(model='custom_model', messages=[
  {
    'role': 'user',
    'content': prompt,
  },
])

print(response.message.content)
