from autogen.agentchat.contrib.multimodal_conversable_agent import MultimodalConversableAgent
from backend.gpt4all_client import GPT4AllClient

SYSTEM_MESSAGE = """
You are an expert system integrator. Your job is to create integration codes and connectors between services.
Write optimized, modular Python code only.
"""

class IntegrationAgent(MultimodalConversableAgent):
    def __init__(self):
        super().__init__(
            name="IntegrationDeveloper",
            system_message=SYSTEM_MESSAGE,
            llm_config=False
        )
        self.model_client = GPT4AllClient()

    async def a_generate_reply(self, messages, sender=None):
        prompt = messages[-1]["content"] if messages else ""
        response = self.model_client.generate([{"role": "user", "content": prompt}])
        return response

def get_integration_agent():
    return IntegrationAgent()
