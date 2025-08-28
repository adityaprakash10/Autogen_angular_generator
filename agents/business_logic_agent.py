from autogen.agentchat.contrib.multimodal_conversable_agent import MultimodalConversableAgent
from backend.gpt4all_client import GPT4AllClient

SYSTEM_MESSAGE = """
You are an expert business logic developer. Your job is to implement backend logic connecting the API and data layers.
Write clean, maintainable Python code only.
"""

class BusinessLogicAgent(MultimodalConversableAgent):
    def __init__(self):
        super().__init__(
            name="BusinessLogicDeveloper",
            system_message=SYSTEM_MESSAGE,
            llm_config=False
        )
        self.model_client = GPT4AllClient()

    async def a_generate_reply(self, messages, sender=None):
        prompt = messages[-1]["content"] if messages else ""
        response = self.model_client.generate([{"role": "user", "content": prompt}])
        return response

def get_business_logic_agent():
    return BusinessLogicAgent()
