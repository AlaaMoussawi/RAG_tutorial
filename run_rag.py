from ollama import chat

pre_prompt = "<|content_start>{}<|content_end><|im_end|><|im_start|>user{}<|im_end|><|im_start|>assistant".format(content, user_query)

