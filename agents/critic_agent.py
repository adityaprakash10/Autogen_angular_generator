from autogen.agentchat.contrib.multimodal_conversable_agent import MultimodalConversableAgent
from backend.gpt4all_client import GPT4AllClient

SYSTEM_MESSAGE = """
You are the central code critic. Your job is to review generated code for correctness, consistency, security, and adherence to requirements.
Return clear JSON status with approve/revise and detailed feedback.
"""

class CriticAgent(MultimodalConversableAgent):
    def __init__(self):
        super().__init__(
            name="Critic",
            system_message=SYSTEM_MESSAGE,
            llm_config=False,
        )
        self.model_client = GPT4AllClient()

    async def a_generate_reply(self, messages, sender=None):
        prompt = messages[-1]["content"] if messages else ""
        response = self.model_client.generate([{"role": "user", "content": prompt}])
        return response

def get_critic_agent():
    return CriticAgent()
