from autogen.agentchat.contrib.multimodal_conversable_agent import MultimodalConversableAgent
from backend.gpt4all_client import GPT4AllClient

SYSTEM_MESSAGE = """
You are an expert machine learning model developer. Your job is to create model definitions and training code from requirements.
Provide clean and runnable Python ML code only.
"""

class ModelDeveloperAgent(MultimodalConversableAgent):
    def __init__(self):
        super().__init__(
            name="ModelDeveloper",
            system_message=SYSTEM_MESSAGE,
            llm_config=False
        )
        self.model_client = GPT4AllClient()

    async def a_generate_reply(self, messages, sender=None):
        prompt = messages[-1]["content"] if messages else ""
        response = self.model_client.generate([{"role": "user", "content": prompt}])
        return response

def get_model_developer_agent():
    return ModelDeveloperAgent()
