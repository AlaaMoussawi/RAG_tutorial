from prepare_content import search_by_query
from ollama import chat
import sys

query = "Tell me about children's rights in Germany."
if len(sys.argv) > 1:
    # raise ValueError("Please pass a query when calling the script.")
    query = sys.argv[1]

context = search_by_query(query)

prompt = "<|content_start>{} \
<|content_end> {}".format(context, query)

response = chat(model='custom_model', messages=[
  {
    'role': 'user',
    'content': prompt,
  },
])

print(response.message.content)