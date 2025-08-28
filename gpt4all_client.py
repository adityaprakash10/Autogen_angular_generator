from gpt4all import GPT4All

class GPT4AllClient:
    def __init__(self, model_path="/Users/adityaprakash/Library/Application Support/nomic.ai/GPT4All/Llama-3.2-1B-Instruct-Q4_0.gguf"):
        self.model = GPT4All(model_path)

    def generate(self, messages):
        prompt = messages[-1]["content"] if messages else ""
        # Use generate() or chat() method depending on gpt4all version
        # Example using generate():
        response = self.model.generate(prompt)
        return response
