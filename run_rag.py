from ollama import chat

query = "Tell me about children's rights in Germany."
if len(sys.argv) > 1:
    # raise ValueError("Please pass a query when calling the script.")
    query = sys.argv[1]

context = search_by_query(query)

# Example failed messages
messages = "<|im_start|>user" \
"{}<|im_end|><|im_start|>assistant" \
"{}<|im_end|>".format("Why is the sky blue?", "Given the information provided, I am unable to answer your question.")

pre_prompt = "<|content_start>{}" \
"<|content_end><|im_end|>{}<|im_start|>user" \
"{}<|im_end|><|im_start|>assistant" \
"".format(context, messages, query)

