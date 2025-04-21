from ollama import chat

pre_prompt = "<|content_start>{}<|content_end><|im_end|><|im_start|>user{}<|im_end|><|im_start|>assistant".format(content, user_query)

query = "Tell me about human rights in Germany."
if len(sys.argv) > 1:
    # raise ValueError("Please pass a query when calling the script.")
    query = sys.argv[1]

