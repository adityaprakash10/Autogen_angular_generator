from autogen.agentchat.contrib.multimodal_conversable_agent import MultimodalConversableAgent
from backend.gpt4all_client import GPT4AllClient

SYSTEM_MESSAGE = """
You are a state management expert. Your task is to generate frontend state management code in TypeScript.
Provide clean and maintainable code.
"""

class StateManagementAgent(MultimodalConversableAgent):
    def __init__(self):
        super().__init__(
            name="StateManager",
            system_message=SYSTEM_MESSAGE,
            llm_config=False,
        )
        self.model_client = GPT4AllClient()

    async def a_generate_reply(self, messages, sender=None):
        prompt = messages[-1]["content"] if messages else ""
        response = self.model_client.generate([{"role": "user", "content": prompt}])
        return response

def get_state_management_agent():
    return StateManagementAgent()
