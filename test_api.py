from gpt4all_client import GPT4AllClient

def main():
    client = GPT4AllClient()
    messages = [{"role": "user", "content": "Write a FastAPI hello world example"}]
    response = client.generate(messages)
    print("Model response:\n", response)

if __name__ == "__main__":
    main()
